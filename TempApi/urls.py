"""
URL configuration for TempApi project.
"""
from django.contrib import admin
from django.urls import path

from TempByLocationApi.views import get_location_weather, get_location_coordinates

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/get-weather/', get_location_weather, name='get_weather'),
    path('api/get-location-coordinates/', get_location_coordinates, name='get_location_coordinates'),

]