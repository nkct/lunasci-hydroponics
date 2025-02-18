from django.db import models
from django.conf import settings

class Hydroponics(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='hydroponics', on_delete=models.CASCADE)
    name = models.CharField(max_length=512, default="Hydroponics")

    def __str__(self):
        return self.name
    
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