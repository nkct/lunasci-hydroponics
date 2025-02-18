from django.shortcuts import render

from rest_framework import permissions, viewsets

from django.contrib.auth.models import User
from lunasci.hydroponics.models import Hydroponics, SensorReading

from lunasci.hydroponics.serializers import HydroponicsSerializer, UserSerializer, SensorReadingSerializer
from lunasci.hydroponics.permissions import IsOwnerOrReadOnly

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class HydroponicsViewSet(viewsets.ModelViewSet):
    queryset = Hydroponics.objects.all().order_by("-created")
    serializer_class = HydroponicsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SensorReadingViewSet(viewsets.ModelViewSet):
    queryset = SensorReading.objects.all().order_by("-created")
    serializer_class = SensorReadingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]