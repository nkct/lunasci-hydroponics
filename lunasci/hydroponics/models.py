from django.db import models
from django.conf import settings

class Hydroponics(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='hydroponics', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'hydroponics'

class SensorReading(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    hydroponics = models.ForeignKey(Hydroponics, related_name='readings', on_delete=models.CASCADE)
    ph = models.FloatField(null=True, blank=True)
    temperature = models.FloatField(null=True, blank=True)
    tds = models.FloatField(null=True, blank=True)
    
    class Meta:
        db_table = 'sensor_reading'