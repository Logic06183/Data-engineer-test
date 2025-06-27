import csv
import os
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from harmoniseproject.models import ClimateDaily, ClimateYearly, ClinicalTrial

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_PATH = os.path.join(BASE_DIR, "C:\\Users\\LUCY\\Documents\\Lucy Gachogu Documents\\HR Files\\Masters Programmes\\University of Pretoria\\IOT Data Analysis\\Data from CSIR\\Iot_data_analysis\\lucygachogu\\sample_data")

class Command(BaseCommand):
    help = 'Ingest and harmonise CSV data into PostgreSQL'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting data ingestion...")
        with transaction.atomic():
            self.load_climate_daily()
            self.load_climate_yearly()
            self.load_clinical_trials()
        self.stdout.write("Data ingestion completed.")

    def load_climate_daily(self):
        filepath = os.path.join(DATA_PATH, "climate_daily.csv")
        with open(filepath, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            ClimateDaily.objects.all().delete()
            for row in reader:
                ClimateDaily.objects.create(
                    station_id=row["station_id"],
                    date=row["date"],
                    temperature=float(row["temperature"]),
                    rainfall=float(row["rainfall"])
                )

    def load_climate_yearly(self):
        filepath = os.path.join(DATA_PATH, "climate_yearly.csv")
        with open(filepath, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            ClimateYearly.objects.all().delete()
            for row in reader:
                ClimateYearly.objects.create(
                    station_id=row["station_id"],
                    year=int(row["year"]),
                    avg_temp=float(row["avg_temp"]),
                    total_rainfall=float(row["total_rainfall"])
                )

    def load_clinical_trials(self):
        files = ["clinical_trial.csv", "clinical_trial_2.csv"]
        ClinicalTrial.objects.all().delete()
        for fname in files:
            with open(os.path.join(DATA_PATH, fname), newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    ClinicalTrial.objects.create(
                        trial_id=row["trial_id"],
                        title=row["title"],
                        status=row["status"],
                        start_date=row["start_date"],
                        end_date=row["end_date"]
                    )
