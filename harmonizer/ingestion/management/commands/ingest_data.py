from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
import pandas as pd
import yaml
from pathlib import Path
from ingestion.models import HarmonizedData


class Command(BaseCommand):
    help = 'Ingests data from CSV file and maps it to a harmonized schema'

    def __init__(self):
        super().__init__()
        self.stats = {
            'total_rows': 0,
            'columns': [],
            'mapped_records': 0,
            'missing_required': 0,
            'type_errors': 0,
            'validation_errors': 0,
            'created': 0,
            'duplicates': 0,
            'insert_errors': 0
        }

    def add_arguments(self, parser):
        parser.add_argument('--csv_file', type=str)
        parser.add_argument('--codebook', type=str)

    def load_codebook(self, codebook_path):
        """Load and validate the codebook for data mapping."""
        try:
            with open(codebook_path, 'r') as file:
                yaml_content = yaml.safe_load(file)
                # Get actual field mappings from nested structure if needed
                if 'fields' in yaml_content:
                    return yaml_content['fields']
                return yaml_content
        except Exception as e:
            raise CommandError(f"Failed to load codebook file: {e}")

    def load_csv_data(self, file_path):
        """Load and validate a CSV file using pandas."""
        try:
            # Check if file exists
            if not Path(file_path).exists():
                raise CommandError(f"CSV file not found: {file_path}")
                
            # Read the CSV file
            df = pd.read_csv(file_path)
            
            # Basic validation
            if df.empty:
                raise CommandError(f"CSV file is empty: {file_path}")
                
            # Remove any completely empty rows or columns
            df = df.dropna(how='all').dropna(axis=1, how='all')
            
            # Update statistics
            self.stats['total_rows'] = len(df)
            self.stats['columns'] = list(df.columns)
            
            # Provide some information about the data
            self.stdout.write(f"Loaded CSV file with {len(df)} rows and {len(df.columns)} columns")
            self.stdout.write(f"Columns found: {', '.join(df.columns)}")
            
            return df
            
        except pd.errors.EmptyDataError:
            raise CommandError(f"CSV file is empty: {file_path}")
        except pd.errors.ParserError as e:
            raise CommandError(f"Invalid CSV format in {file_path}: {str(e)}")
        except Exception as e:
            raise CommandError(f"Failed to load CSV file {file_path}: {str(e)}")

    def apply_transformation(self, value, field_config, field_name=None):
        """Apply transformations to a value based on field configuration."""
        if value is None or pd.isna(value):
            if field_config.get('required', False):
                self.stdout.write(self.style.WARNING(
                    f"Required field '{field_name}' has null value"
                ))
            return None
            
        # Apply type conversion
        datatype = field_config.get('datatype')
        if datatype:
            try:
                if datatype == 'integer':
                    return int(float(value))
                elif datatype == 'float':
                    return float(value)
                elif datatype == 'string':
                    return str(value)
                elif datatype == 'date':
                    try:
                        return pd.to_datetime(value).strftime('%Y-%m-%d')
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(
                            f"Failed to parse date '{value}' for field '{field_name}': {str(e)}"
                        ))
                        self.stats['type_errors'] += 1
                        return None
            except (ValueError, TypeError) as e:
                self.stdout.write(self.style.WARNING(
                    f"Failed to convert '{value}' to {datatype} for field '{field_name}': {str(e)}"
                ))
                self.stats['type_errors'] += 1
                return None
                
        # Apply value transformations
        if 'transformations' in field_config:
            transforms = field_config['transformations']
            if transforms and str(value) in transforms:
                value = transforms[str(value)]
                
        # Apply allowed values validation
        if 'allowed_values' in field_config:
            allowed = field_config['allowed_values']
            if value not in allowed:
                self.stdout.write(self.style.WARNING(
                    f"Value '{value}' not in allowed values {allowed} for field '{field_name}'"
                ))
                self.stats['validation_errors'] += 1
                return None
                
        return value

    def detect_data_type(self, columns):
        """Detect whether this is clinical or climate data."""
        clinical_indicators = ['patient_id', 'subject_id', 'adverse_event']
        climate_indicators = ['daily_temp_c', 'precip_mm', 'humidity_pct', 'aqi']
        
        for indicator in clinical_indicators:
            if indicator in columns:
                return 'clinical'
        for indicator in climate_indicators:
            if indicator in columns:
                return 'climate'
        return 'unknown'

    def map_data_using_codebook(self, df, codebook):
        """Map data from source format to harmonized format using schema."""
        mapped_data = []
        error_count = 0
        row_index = 0

        # Detect data type
        data_type = self.detect_data_type(df.columns)
        self.stdout.write(f"Detected data type: {data_type}")

        # Field mappings for different data sources
        field_mappings = {
            'participant_id': ['patient_id', 'subject_id'],
            'visit_date': ['visit_date', 'date'],
            'location_id': ['site_location', 'center_id', 'location_id'],
            'age': ['age', 'age_years'],
            'sex': ['sex'],
            'study_group': ['arm', 'trial_group'],
            'body_temperature': ['temperature_c'],
            'systolic_bp': ['systolic_bp'],
            'diastolic_bp': ['diastolic_bp'],
            'adverse_event': ['adverse_event'],
            'temperature': ['daily_temp_c'],
            'precipitation': ['precip_mm'],
            'humidity': ['humidity_pct'],
            'air_quality_index': ['aqi']
        }
        
        for _, row in df.iterrows():
            row_index += 1
            try:
                harmonized_record = {}
                
                # Map each field from source to harmonized schema
                for harmonized_field, source_fields in field_mappings.items():
                    value = None
                    # Try each possible source field name
                    for source_field in source_fields:
                        if source_field in df.columns:
                            value = row[source_field]
                            if pd.notna(value):  # Skip empty/nan values
                                if harmonized_field == 'sex' and isinstance(value, str):
                                    # Transform sex values
                                    value = {'M': 'Male', 'F': 'Female'}.get(value, value)
                                if harmonized_field == 'study_group' and isinstance(value, str):
                                    # Transform study group values
                                    value = {'Control': 'Placebo'}.get(value, value)
                                harmonized_record[harmonized_field] = value
                                break
                
                # Different validation for clinical vs climate data
                if data_type == 'clinical':
                    required_fields = ['participant_id', 'visit_date', 'location_id']
                else:  # climate data
                    # For climate data, we'll update existing records that match date and location
                    required_fields = ['visit_date', 'location_id']
                    
                missing = [f for f in required_fields if f not in harmonized_record]
                if missing:
                    self.stdout.write(self.style.WARNING(
                        f"Row {row_index}: Skipping record due to missing required fields: {', '.join(missing)}"
                    ))
                    self.stats['missing_required'] += 1
                    continue

                # For climate data, we need to update existing records rather than create new ones
                if data_type == 'climate':
                    try:
                        # Find matching clinical records and update them with climate data
                        matches = HarmonizedData.objects.filter(
                            visit_date=harmonized_record['visit_date'],
                            location_id=harmonized_record['location_id']
                        )
                        
                        for match in matches:
                            # Update climate-related fields
                            for field in ['temperature', 'precipitation', 'humidity', 'air_quality_index']:
                                if field in harmonized_record:
                                    setattr(match, field, harmonized_record[field])
                            match.save()
                            self.stats['created'] += 1  # In this case, "created" means "updated"
                            
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(
                            f"Row {row_index}: Failed to update clinical records with climate data: {str(e)}"
                        ))
                        self.stats['insert_errors'] += 1
                        
                else:  # clinical data
                    mapped_data.append(harmonized_record)
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f"Row {row_index}: Failed to process record: {str(e)}"
                ))
                error_count += 1
        
        if error_count > 0:
            self.stdout.write(self.style.WARNING(
                f"Encountered errors in {error_count} out of {row_index} records"
            ))
        
        self.stats['mapped_records'] = len(mapped_data)
        return mapped_data

    def print_summary(self):
        """Print a detailed summary of the ingestion process."""
        self.stdout.write("\n=== Ingestion Summary ===")
        
        # Input data statistics
        self.stdout.write(f"\nInput Data:")
        self.stdout.write(f"- Total rows in CSV: {self.stats['total_rows']}")
        self.stdout.write(f"- Columns found: {', '.join(self.stats['columns'])}")
        
        # Transformation statistics
        self.stdout.write(f"\nData Transformation:")
        self.stdout.write(f"- Records successfully mapped: {self.stats['mapped_records']}")
        self.stdout.write(f"- Records with missing required fields: {self.stats['missing_required']}")
        self.stdout.write(f"- Type conversion errors: {self.stats['type_errors']}")
        self.stdout.write(f"- Validation errors: {self.stats['validation_errors']}")
        
        # Database insertion statistics
        self.stdout.write(f"\nDatabase Insertion:")
        self.stdout.write(f"- Records created: {self.stats['created']}")
        self.stdout.write(f"- Duplicates skipped: {self.stats['duplicates']}")
        self.stdout.write(f"- Insert errors: {self.stats['insert_errors']}")
        
        # Final status
        total_errors = (self.stats['missing_required'] + self.stats['type_errors'] + 
                       self.stats['validation_errors'] + self.stats['insert_errors'])
        
        self.stdout.write("\nFinal Status:")
        if total_errors == 0:
            self.stdout.write(self.style.SUCCESS("✓ Ingestion completed successfully"))
        else:
            self.stdout.write(self.style.ERROR(
                f"✗ Ingestion completed with {total_errors} errors"
            ))
        self.stdout.write("=" * 25)

    def insert_data(self, mapped_data):
        """Insert mapped data into the Django model."""
        with transaction.atomic():
            for record in mapped_data:
                try:
                    # Check if a record with the same unique identifiers exists
                    existing = HarmonizedData.objects.filter(
                        participant_id=record['participant_id'],
                        visit_date=record['visit_date'],
                        location_id=record['location_id']
                    ).first()
                    
                    if existing:
                        self.stdout.write(self.style.WARNING(
                            f"Skipping duplicate record for participant {record['participant_id']} "
                            f"on {record['visit_date']} at {record['location_id']}"
                        ))
                        self.stats['duplicates'] += 1
                        continue
                    
                    HarmonizedData.objects.create(**record)
                    self.stats['created'] += 1
                    
                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f"Error inserting record: {str(e)}\nRecord data: {record}"
                    ))
                    self.stats['insert_errors'] += 1

    def handle(self, *args, **kwargs):
        try:
            # Load data sources
            csv_file = kwargs['csv_file']
            codebook_path = kwargs['codebook']
            
            # Load codebook and data
            codebook = self.load_codebook(codebook_path)
            data = self.load_csv_data(csv_file)
            
            # Map the data
            mapped_data = self.map_data_using_codebook(data, codebook)
            
            # Insert the mapped data into the database
            self.insert_data(mapped_data)
            
            # Print the final summary
            self.print_summary()
            
        except Exception as e:
            raise CommandError(f"Failed to process data: {str(e)}")
