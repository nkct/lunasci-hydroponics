"""
URL configuration for lunasci project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

from lunasci.hydroponics import views

router = routers.SimpleRouter()
router.register(r'users', views.UserViewSet)
router.register(r'hydroponics', views.HydroponicsViewSet)
router.register(r'sensor_readings', views.SensorReadingViewSet)

urlpatterns = [
    path('', views.APIRoot.as_view()),
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api-schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api-docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
]
