"""
This module defines serializers for converting model instances to and from JSON format.

It provides serializers for:
    - User: Serializing Django user instances.
    - Hydroponics: Serializing hydroponics system instances.
    - SensorReading: Serializing sensor reading instances.
"""
from django.conf import settings

from rest_framework import serializers
from rest_framework.reverse import reverse

from lunasci.hydroponics.models import Hydroponics, SensorReading

class HydroponicsSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Hydroponics model.

    This serializer converts Hydroponics instances into a JSON representation including:
        - The detail view URL.
        - Instance ID, creation timestamp, and name.
        - The username of the owner.
        - A list of hyperlinks to the latest sensor readings.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    sensor_readings = serializers.SerializerMethodField()

    def get_sensor_readings(self, obj):
        """
        Retrieve hyperlinks for the latest sensor readings associated with the Hydroponics instance.
        """
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
    """
    Serializer for the User model.

    This serializer converts User instances into a JSON representation including:
        - The detail view URL.
        - User ID, date joined, and username.
        - Hyperlinks to the hydroponics instances owned by the user.
    """
    hydroponics = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='hydroponics-detail',
        read_only=True
    )

    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ['url', 'id', 'date_joined', 'username', 'hydroponics']

class SensorReadingSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the SensorReading model.

    This serializer converts SensorReading instances into a JSON representation including:
        - The detail view URL.
        - Instance ID, creation timestamp, and associated hydroponics instance.
        - Sensor measurements: pH, temperature, and total dissolved solids (TDS).
    """
    class Meta:
        model = SensorReading
        fields = ['url', 'id', 'created', 'hydroponics', 'ph', 'temperature', 'tds']
