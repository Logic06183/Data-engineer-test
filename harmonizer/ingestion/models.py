from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class HarmonizedData(models.Model):
    # Patient/Subject Identifier
    participant_id = models.CharField(
        max_length=100,
        help_text="Unique participant identifier"
    )

    # Visit Information
    visit_date = models.DateField(
        help_text="Date of clinical visit"
    )

    # Location Information
    location_id = models.CharField(
        max_length=100,
        help_text="Clinical site location identifier"
    )

    # Demographic Information
    age = models.IntegerField(
        null=True,
        blank=True,
        help_text="Age of participant in years"
    )

    SEX_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
        ('Unknown', 'Unknown')
    ]
    sex = models.CharField(
        max_length=10,
        choices=SEX_CHOICES,
        null=True,
        blank=True,
        help_text="Biological sex"
    )

    # Study Group Information
    study_group = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Study group or arm assignment"
    )

    # Clinical Measurements
    body_temperature = models.FloatField(
        null=True,
        blank=True,
        help_text="Body temperature in Celsius"
    )

    systolic_bp = models.IntegerField(
        null=True,
        blank=True,
        help_text="Systolic blood pressure in mmHg"
    )

    diastolic_bp = models.IntegerField(
        null=True,
        blank=True,
        help_text="Diastolic blood pressure in mmHg"
    )

    # Outcome Information
    ADVERSE_EVENT_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No')
    ]
    adverse_event = models.CharField(
        max_length=3,
        choices=ADVERSE_EVENT_CHOICES,
        null=True,
        blank=True,
        help_text="Whether an adverse event occurred"
    )

    # Climate Data
    temperature = models.FloatField(
        null=True,
        blank=True,
        help_text="Daily mean temperature in Celsius"
    )

    precipitation = models.FloatField(
        null=True,
        blank=True,
        help_text="Daily precipitation in mm"
    )

    humidity = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Daily mean relative humidity in percent"
    )

    air_quality_index = models.IntegerField(
        null=True,
        blank=True,
        help_text="Air Quality Index value"
    )

    class Meta:
        verbose_name = "Harmonized Data"
        verbose_name_plural = "Harmonized Data"
        # Ensure unique participant visits
        unique_together = ['participant_id', 'visit_date', 'location_id']

    def __str__(self):
        return f"Participant {self.participant_id} - Visit {self.visit_date}"
