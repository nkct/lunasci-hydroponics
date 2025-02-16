from rest_framework import serializers

from django.contrib.auth.models import User
from lunasci.hydroponics.models import Hydroponics

class HydroponicsSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
        model = Hydroponics
        fields = ['url', 'created', 'owner']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    hydroponics = serializers.HyperlinkedRelatedField(many=True, view_name='hydroponics-detail', read_only=True)
    
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'hydroponics']