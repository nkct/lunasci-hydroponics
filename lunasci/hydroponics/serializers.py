"""
This module defines serializers for converting model instances to and from JSON format.

It provides serializers for:
    - User: Serializing Django user instances.
    - Hydroponics: Serializing hydroponics system instances.
    - SensorReading: Serializing sensor reading instances.
"""

from rest_framework import serializers
from rest_framework.reverse import reverse

from django.contrib.auth.models import User
from lunasci.hydroponics.models import Hydroponics, SensorReading

class HydroponicsSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    sensor_readings = serializers.SerializerMethodField()

    def get_sensor_readings(self, obj):
        request = self.context.get('request')
        # Limit the sensor readings to the first 10
        sensor_readings = obj.readings.all().order_by('-created')[:10]
        # Return a list of hyperlinks to the sensor reading detail views
        return [
            reverse('sensorreading-detail', kwargs={'pk': reading.pk}, request=request)
            for reading in sensor_readings
        ]
    
    class Meta:
        model = Hydroponics
        fields = ['url', 'id', 'created', 'name', 'owner', 'sensor_readings']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    hydroponics = serializers.HyperlinkedRelatedField(many=True, view_name='hydroponics-detail', read_only=True)
    
    class Meta:
        model = User
        fields = ['url', 'id', 'date_joined', 'username', 'hydroponics']

class SensorReadingSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = SensorReading
        fields = ['url', 'id', 'created', 'hydroponics', 'ph', 'temperature', 'tds']