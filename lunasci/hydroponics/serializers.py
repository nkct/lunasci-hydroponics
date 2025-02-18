from rest_framework import serializers

from django.contrib.auth.models import User
from lunasci.hydroponics.models import Hydroponics, SensorReading

class HydroponicsSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    sensor_readings = serializers.HyperlinkedRelatedField(many=True, view_name='sensorreading-detail', read_only=True, source='readings')
    
    class Meta:
        model = Hydroponics
        fields = ['url', 'id', 'created', 'owner', 'sensor_readings']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    hydroponics = serializers.HyperlinkedRelatedField(many=True, view_name='hydroponics-detail', read_only=True)
    
    class Meta:
        model = User
        fields = ['url', 'id', 'date_joined', 'username', 'hydroponics']

class SensorReadingSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = SensorReading
        fields = ['url', 'id', 'created', 'hydroponics', 'ph', 'temperature', 'tds']