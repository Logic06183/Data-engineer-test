from django.db import models

# Create your models here.

class Climate_daily(models.Model):

    title = models.CharField(max_length=100)
    site_id = models.FloatField()
    date = models.DateField()
    daily_temp_c = models.FloatField()
    precip_mm = models.IntegerField()
    humidity_pct = models.IntegerField()
    location_id = models.CharField(max_length=50)

