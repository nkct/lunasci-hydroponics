"""
This module defines REST API viewsets and filters for the hydroponics application.

It includes viewsets for managing:
    - Users (UserViewSet)
    - Hydroponics systems (HydroponicsViewSet)
    - Sensor readings (SensorReadingViewSet)

It also defines custom filter classes for these resources to enable flexible query parameters.
"""

from django.contrib.auth import get_user_model

from rest_framework import permissions, viewsets, generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
import django_filters

from lunasci.hydroponics.models import Hydroponics, SensorReading

from lunasci.hydroponics.serializers import (
    HydroponicsSerializer,
    UserSerializer,
    SensorReadingSerializer
)
from lunasci.hydroponics.permissions import IsOwnerOrReadOnly, IsSelfOrReadOnly

User = get_user_model()

class UserFilter(django_filters.FilterSet):
    """
    Provides filtering options for the User model.
    
    Filters:
        date_joined: Allows filtering users based on a date range.
        id: Allows filtering based on exact, greater than or equal, and less than or equal values.
        username: Allows filtering based on exact match, containment, and prefix.
    """
    date_joined = django_filters.DateFromToRangeFilter()

    class Meta:
        model = User
        fields = {
            'id': ['exact', 'gte', 'lte'], 
            'username': ['exact', 'icontains', 'istartswith'],
        }

class HydroponicsFilter(django_filters.FilterSet):
    """
    Provides filtering options for the Hydroponics model.
    
    Filters:
        created: Allows filtering hydroponics instances based on a date range.
        id: Allows filtering based on exact, greater than or equal, and less than or equal values.
        name: Allows filtering based on exact match and case-insensitive containment or prefix.
        owner__username: Allows filtering based on the owner's username.
    """
    created = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Hydroponics
        fields = {
            'id': ['exact', 'gte', 'lte'],
            'name': ['exact', 'icontains', 'istartswith'],
            'owner__username': ['exact', 'icontains', 'istartswith'],
        }

class SensorReadingFilter(django_filters.FilterSet):
    """
    Provides filtering options for the SensorReading model.
    
    Filters:
        created: Allows filtering sensor readings based on a date range.
        id: Allows filtering based on exact, greater than or equal, and less than or equal values.
        hydroponics__name: Allows filtering sensor readings by the name of the related hydroponics.
        ph, temperature, tds: Allows filtering based on ==, >= and <= operators.
    """
    created = django_filters.DateFromToRangeFilter()

    class Meta:
        model = SensorReading
        fields = {
            'id': ['exact', 'gte', 'lte'],
            'hydroponics__name': ['exact', 'icontains', 'istartswith'],
            'ph': ['exact', 'gte', 'lte'],
            'temperature': ['exact', 'gte', 'lte'],
            'tds': ['exact', 'gte', 'lte'],
        }

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user accounts.

    This viewset provides endpoints for listing user profiles as well as retrieving,
    updating, or deleting a user's own profile. The following behaviors are enforced:

      - Unauthenticated users can list all user profiles (with limited public fields).
      - Authenticated users can only retrieve, update, or delete their own profile.
      - Creation of new users via this endpoint is disallowed.

    Adding and managing users can be done trough the admin panel at /admin
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSelfOrReadOnly]
    ordering = ['date_joined']
    ordering_fields = ['id', 'date_joined', 'username']
    filterset_fields = {
        'id': ['exact', 'gte', 'lte'], 
        'date_joined': ['exact', 'gte', 'lte'], 
        'username': ['exact', 'gte', 'lte'],
    }

class HydroponicsViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Hydroponics instances.
    
    Provides operations to list, retrieve, create, update, and delete hydroponics 
    systems. Only authenticated users can create or update, and only the owner 
    of a hydroponics instance is allowed to modify it.
    """
    queryset = Hydroponics.objects.all()
    serializer_class = HydroponicsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    ordering = ['created']
    ordering_fields = '__all__'
    filterset_class = HydroponicsFilter

    def perform_create(self, serializer):
        """
        Automatically assigns the currently authenticated user as the owner 
        of the hydroponics instance upon creation.
        """
        serializer.save(owner=self.request.user)

class SensorReadingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing SensorReading instances.
    
    Provides operations to list, retrieve, create, update, and delete sensor 
    readings. Access is allowed for both authenticated and unauthenticated users,
    but modification rights are controlled by the configured permissions.
    """
    queryset = SensorReading.objects.all()
    serializer_class = SensorReadingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    ordering = ['created']
    ordering_fields = '__all__'
    filterset_class = SensorReadingFilter

class APIRoot(generics.GenericAPIView):
    """
    Hydroponics API Entry Point.

    This is the root of the Hydroponics API, which offers an interface 
    for managing hydroponic systems, monitoring sensor readings, and handling user accounts.
    """

    def get(self, request, *args, **kwargs):
        """
        Return a JSON response with hyperlinks to the main API endpoints.
        """
        return Response({
            'users': reverse('user-list', request=request),
            'hydroponics': reverse('hydroponics-list', request=request),
            'sensor_readings': reverse('sensorreading-list', request=request),
            'admin': reverse('admin:index', request=request),
            'api-schema': reverse('schema', request=request),
            'api-docs': reverse('docs', request=request),
        })
