"""
Database model.
"""
from django.db import models


class HarmonizedRecord(models.Model):
    """Class representing Harmonized model"""

    participant_id = models.CharField(max_length=64)
    visit_date = models.DateField(null=True, blank=True)
    location_id = models.CharField(max_length=64)

    age = models.IntegerField(null=True, blank=True)
    sex = models.CharField(max_length=16, null=True, blank=True)
    study_group = models.CharField(max_length=64, null=True, blank=True)

    body_temperature = models.FloatField(null=True, blank=True)
    systolic_bp = models.IntegerField(null=True, blank=True)
    diastolic_bp = models.IntegerField(null=True, blank=True)
    adverse_event = models.CharField(max_length=8, null=True, blank=True)

    temperature = models.FloatField(null=True, blank=True)
    precipitation = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    air_quality_index = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.participant_id} @ {self.visit_date} ({self.location_id})"
