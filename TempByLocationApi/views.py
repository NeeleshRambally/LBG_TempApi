from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
import logging

from TempByLocationApi.service import LocationService

logger = logging.getLogger(__name__)

@csrf_exempt
@api_view(['POST'])
def get_location_weather(request):
    """
    View to fetch latitude, longitude, and weather data for a location.
    """
    logger.info("Received request for location weather data.")

    location = request.GET.get('location', '')

    if not location:
        logger.warning("No location parameter provided.")
        return JsonResponse({'error': 'Location parameter is required.'}, status=400)

    # Use the service to fetch and save coordinates
    coordinates_result = LocationService.fetch_and_save_location_coordinates(location)

    if coordinates_result:
        logger.info(f"Successfully retrieved and saved location: {location}")

        # Fetch weather data using the coordinates
        weather_data = LocationService.get_weather_data(coordinates_result['latitude'], coordinates_result['longitude'])

        if weather_data:
            logger.info(f"Successfully fetched weather data for location: {location}")
            return Response({
                'location': coordinates_result['location'],
                'latitude': coordinates_result['latitude'],
                'longitude': coordinates_result['longitude'],
                'weather': weather_data
            })
        else:
            logger.warning("Failed to fetch weather data.")
            return Response({'error': 'Failed to fetch weather data.'}, status=404)
    else:
        logger.warning("Failed to fetch and save location coordinates.")
        return Response({'error': 'Failed to fetch and save location coordinates.'}, status=404)


@csrf_exempt
@api_view(['POST'])
def get_location_coordinates(request):
    """
    View to fetch only latitude and longitude for a location without weather data.
    """
    logger.info("Received request for location coordinates only.")

    location = request.GET.get('location', '')

    if not location:
        logger.warning("No location parameter provided.")
        return JsonResponse({'error': 'Location parameter is required.'}, status=400)

    coordinates_result = LocationService.fetch_and_save_location_coordinates(location)

    if coordinates_result:
        logger.info(f"Successfully retrieved and saved location: {location}")
        return Response(coordinates_result)
    else:
        logger.warning("Failed to fetch and save location coordinates.")
        return Response({'error': 'Failed to fetch and save location coordinates.'}, status=404)
