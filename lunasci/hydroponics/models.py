"""
This module defines the data models for the hydroponics system.

It contains:
    - Hydroponics: Represents a hydroponic system, including the owner, creation time, and name.
    - SensorReading: Represents sensor data (pH, temperature, TDS) recorded in a hydroponics system.
"""

from django.db import models
from django.conf import settings

class Hydroponics(models.Model):
    """
    Represents a hydroponic system instance.

    Attributes:
        created (datetime): The timestamp when the hydroponic system was created.
        owner (ForeignKey): The user who owns this hydroponic system.
        name (str): A human-readable name for the hydroponic system.
    """
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='hydroponics',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=512, default="Hydroponics")

    def __str__(self):
        """
        Returns the name of the hydroponic system.
        """
        return self.name

    class Meta:
        db_table = 'hydroponics'
        indexes = [
            models.Index(fields=["created"]),
            models.Index(fields=["owner"]),
        ]

class SensorReading(models.Model):
    """
    Represents a sensor reading taken in a hydroponic system.

    Attributes:
        created (datetime): The timestamp when the sensor reading was recorded.
        hydroponics (ForeignKey): The hydroponic system to which this sensor reading belongs.
        ph (float): The pH value recorded by the sensor.
        temperature (float): The temperature recorded by the sensor.
        tds (float): The total dissolved solids recorded by the sensor.
    """
    created = models.DateTimeField(auto_now_add=True)
    hydroponics = models.ForeignKey(Hydroponics, related_name='readings', on_delete=models.CASCADE)
    ph = models.FloatField(null=True, blank=True)
    temperature = models.FloatField(null=True, blank=True)
    tds = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'sensor_reading'
        indexes = [
            models.Index(fields=["created"]),
            models.Index(fields=["hydroponics"]),
            models.Index(fields=["ph"]),
            models.Index(fields=["temperature"]),
            models.Index(fields=["tds"]),
        ]
