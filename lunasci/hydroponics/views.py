from django.shortcuts import render

from rest_framework import permissions, viewsets
import django_filters

from django.contrib.auth.models import User
from lunasci.hydroponics.models import Hydroponics, SensorReading

from lunasci.hydroponics.serializers import HydroponicsSerializer, UserSerializer, SensorReadingSerializer
from lunasci.hydroponics.permissions import IsOwnerOrReadOnly

class UserFilter(django_filters.FilterSet):
    date_joined = django_filters.DateFromToRangeFilter()
    
    class Meta:
        model = User
        fields = {
            'id': ['exact', 'gte', 'lte'], 
            'username': ['exact', 'icontains', 'istartswith'],
        }

class HydroponicsFilter(django_filters.FilterSet):
    created = django_filters.DateFromToRangeFilter()
    
    class Meta:
        model = Hydroponics
        fields = {
            'id': ['exact', 'gte', 'lte'],
            'owner__username': ['exact', 'icontains', 'istartswith'],
        }

class SensorReadingFilter(django_filters.FilterSet):
    created = django_filters.DateFromToRangeFilter()
    
    class Meta:
        model = SensorReading
        fields = {
            'id': ['exact', 'gte', 'lte'],
            'ph': ['exact', 'gte', 'lte'],
            'temperature': ['exact', 'gte', 'lte'],
            'tds': ['exact', 'gte', 'lte'],
        }

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering = ['date_joined']
    ordering_fields = ['id', 'date_joined', 'username']
    filterset_fields = {
        'id': ['exact', 'gte', 'lte'], 
        'date_joined': ['exact', 'gte', 'lte'], 
        'username': ['exact', 'gte', 'lte'],
    }

class HydroponicsViewSet(viewsets.ModelViewSet):
    queryset = Hydroponics.objects.all()
    serializer_class = HydroponicsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    ordering = ['created']
    ordering_fields = '__all__'
    filterset_class = HydroponicsFilter

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SensorReadingViewSet(viewsets.ModelViewSet):
    queryset = SensorReading.objects.all()
    serializer_class = SensorReadingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    ordering = ['created']
    ordering_fields = '__all__'
    filterset_class = SensorReadingFilter
