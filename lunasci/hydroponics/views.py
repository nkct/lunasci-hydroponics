from rest_framework import permissions, viewsets
import django_filters

from django.contrib.auth.models import User
from lunasci.hydroponics.models import Hydroponics, SensorReading

from lunasci.hydroponics.serializers import HydroponicsSerializer, UserSerializer, SensorReadingSerializer
from lunasci.hydroponics.permissions import IsOwnerOrReadOnly

class UserFilter(django_filters.FilterSet):
    """
    Provides filtering options for the User model.
    
    Filters:
        date_joined: Allows filtering users based on a date range.
        id: Allows filtering based on exact, greater than or equal, and less than or equal values.
        username: Allows filtering based on exact match, case-insensitive containment, and case-insensitive prefix.
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
        hydroponics__name: Allows filtering sensor readings by the name of the associated hydroponics system.
        ph, temperature, tds: Allows filtering based on exact, greater than or equal, and less than or equal values.
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
    ViewSet for listing, retrieving, creating, updating, and deleting User instances.
    
    This viewset uses the UserSerializer for serializing user data and restricts 
    access to authenticated users. It also allows filtering and ordering based on 
    specified fields.
    """
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
