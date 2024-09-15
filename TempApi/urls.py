"""
URL configuration for TempApi project.
"""
from django.contrib import admin
from django.urls import path, include

from TempByLocationApi.views import get_location_weather, get_location_coordinates

urlpatterns = [
    path('admin/', admin.site.urls),

    #Gets the lat and long of a entered location
    #http://localhost:8000/api/get-coordinates/?location=New+York
    path('api/get-coordinates/', get_location_weather, name='get_location_weather'),
    path('api/get-location-coordinates/', get_location_coordinates, name='get_location_coordinates'),

]