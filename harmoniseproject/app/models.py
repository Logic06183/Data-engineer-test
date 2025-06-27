from django.db import models

class ClimateDaily(models.Model):
    station_id = models.CharField(max_length=20)
    date = models.DateField()
    temperature = models.FloatField()
    rainfall = models.FloatField()

class ClimateYearly(models.Model):
    station_id = models.CharField(max_length=20)
    year = models.IntegerField()
    avg_temp = models.FloatField()
    total_rainfall = models.FloatField()

class ClinicalTrial(models.Model):
    trial_id = models.CharField(max_length=50, unique=True)
    title = models.TextField()
    status = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
