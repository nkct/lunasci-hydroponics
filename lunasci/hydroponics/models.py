from django.db import models

# Create your models here.

class Hydroponics(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='hydroponics', on_delete=models.CASCADE)
    
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