import csv
from datetime import datetime
import yaml
from django.core.management.base import BaseCommand

from data_ingestion.settings import SAMPLE_DATA_DIR
from data_ingestion.models import HarmonizedRecord


class Command(BaseCommand):
    help = "Ingest and harmonize clinical or climate data"

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv_file',
            required=True,
            help='Path to the CSV data file'
        )
        parser.add_argument(
            '--codebook',
            required=True,
            help='Path to the YAML codebook'
        )

    def handle(self, *args, **options):
        csv_path = SAMPLE_DATA_DIR / options['csv_file']
        schema_path = (
            SAMPLE_DATA_DIR / 'harmonized_clinical_schema.yaml'
        )

        try:
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema = yaml.safe_load(f)
        except FileNotFoundError as e:
            self.stderr.write(f"❌ File not found: {e.filename}")
            return

        self.stdout.write("📘 Loaded codebook")
        self.stdout.write("📘 Loaded harmonized schema")

        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            csv_columns = reader.fieldnames

        # Infer source name by checking if any of the codebook fields' 'codebook_name'
        # matches the CSV columns. This helps identify which source dataset being processed.
        # The 'source_name' must correspond to a key in schema['fields'][field]['source_mappings']
        source_name = None
        for field_meta in schema['fields'].values():
            source_mappings = field_meta.get('source_mappings', {})
            for src_name, src_field in source_mappings.items():
                if src_field in csv_columns:
                    source_name = src_name
                    break
            if source_name:
                break

        if not source_name:
            self.stderr.write(
                "❌ Could not infer source_name from CSV columns "
                "and schema source mappings."
            )
            return

        field_mappings = self.build_mappings(schema['fields'], source_name)

        records_created = 0
        errors = 0

        # Process each CSV row,
        # transform data to harmonized schema and save to DB
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for i, row in enumerate(reader, 1):
                try:
                    harmonized_data = self.transform_row(
                        row,
                        field_mappings,
                        schema['fields'],
                        source_name
                    )

                    location_id = harmonized_data.get('location_id')
                    visit_date = harmonized_data.get('visit_date')

                    if location_id is None:
                        raw_loc = (
                            row.get('location_id')
                            or row.get('site_id')
                            or row.get('center_id')
                        )
                        location_id = raw_loc if raw_loc else None
                        self.stdout.write(f"✅ row: {location_id}")

                    if visit_date is None:
                        raw_date = row.get('visit_date') or row.get('date')
                        try:
                            visit_date = (
                                datetime.strptime(raw_date, "%Y-%m-%d").date()
                                if raw_date else None
                            )
                        except (ValueError, TypeError) as e:
                            self.stderr.write(f"⚠️ Invalid date format in row {i}: {e}")
                            visit_date = None

                    if location_id is not None and visit_date is not None:
                        unique_filter = {
                            'location_id': location_id,
                            'visit_date': visit_date,
                        }

                        HarmonizedRecord.objects.update_or_create(
                            **unique_filter,
                            defaults=harmonized_data
                        )
                        records_created += 1
                    else:
                        self.stderr.write(
                            f"⚠️ Skipping row {i}: "
                            f"missing required keys for unique filter —\n"
                            f"    location_id: {location_id},\n"
                            f"    visit_date: {visit_date}"
                        )
                        errors += 1

                except (KeyError, ValueError, TypeError) as e:
                    self.stderr.write(f"❌ Known error processing row {i}: {e}")
                    errors += 1

                except Exception as e:
                    self.stderr.write(
                        f"❌ Unexpected error processing row {i}: {e}")
                    errors += 1


        self.stdout.write(f"\n✅ Successfully ingested {records_created} records.")
        self.stdout.write(f"⚠️ {errors} records failed.")

    def build_mappings(self, schema_fields, source_name):
        """
        Build a mapping dict from harmonized schema fields (target) 
        to source CSV column names based on source_mappings for source_name.
        """
        mappings = {}
        for target_field, meta in schema_fields.items():
            source_mappings = meta.get('source_mappings', {})
            source_field = source_mappings.get(source_name)
            if source_field:
                mappings[target_field] = source_field
            else:
                print(
                    f"⚠️ No source mapping for '{target_field}' from source "
                    f"'{source_name}', will be None."
                )
        return mappings

    def transform_row(self, row, mappings, schema_fields, source_name):
        """
        Transform a single CSV row dictionary into a harmonized data dictionary
        by applying mappings, type conversions, and transformations defined in schema.
        """
        transformed = {}
        for target_field, source_field in mappings.items():
            value = row.get(source_field)
            meta = schema_fields[target_field]

            if value is None:
                print(
                    f"⚠️ Field '{source_field}' missing in row; "
                    f"setting '{target_field}' to None"
                )
                transformed[target_field] = None
                continue

            transformations = meta.get('transformations', {}).get(source_name)
            if transformations and value in transformations:
                value = transformations[value]

            datatype = meta['datatype']
            if value == '':
                transformed[target_field] = None
                continue

            try:
                if datatype == 'integer':
                    transformed[target_field] = int(value)
                elif datatype == 'float':
                    transformed[target_field] = float(value)
                elif datatype == 'date':
                    # Assuming ISO date format YYYY-MM-DD
                    transformed[target_field] = (
                        datetime.strptime(value, "%Y-%m-%d").date()
                    )
                else:
                    transformed[target_field] = str(value)
            except Exception as e:
                raise ValueError(
                    f"Invalid data type for '{target_field}': '{value}' "
                    f"as {datatype} — {e}"
                ) from e


        return transformed
