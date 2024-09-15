import unittest

from unittest.mock import patch, MagicMock
from django.test import TestCase
from TempByLocationApi.service import LocationService
from TempByLocationApi.models import Location



class LocationServiceTest(TestCase):

    @patch('TempByLocationApi.service.requests.get')
    @patch('TempByLocationApi.service.Location.objects.get')
    def test_fetch_and_save_location_coordinates_existing_location(self, mock_get, mock_requests_get):
        # Test case where location exists in the database
        mock_location = Location(name='NEW YORK', latitude='40.7128', longitude='-74.0060')
        mock_get.return_value = mock_location

        result = LocationService.fetch_and_save_location_coordinates('New York')

        self.assertEqual(result['location'], 'NEW YORK')
        self.assertEqual(result['latitude'], '40.7128')
        self.assertEqual(result['longitude'], '-74.0060')

        mock_get.assert_called_once_with(name='NEW YORK')
        mock_requests_get.assert_not_called()

    @patch('TempByLocationApi.service.requests.get')
    @patch('TempByLocationApi.service.Location.objects.update_or_create')
    def test_fetch_and_save_location_coordinates_new_location(self, mock_update_or_create, mock_requests_get):
        # Test case where location does not exist in the database, and we need to fetch from the API
        mock_requests_get.return_value.status_code = 200
        mock_requests_get.return_value.json.return_value = [
            {'lat': '34.0522', 'lon': '-118.2437'}
        ]
        mock_update_or_create.return_value = (MagicMock(), True)  # Simulate object creation

        result = LocationService.fetch_and_save_location_coordinates('Los Angeles')

        self.assertEqual(result['location'], 'LOS ANGELES')
        self.assertEqual(result['latitude'], '34.0522')
        self.assertEqual(result['longitude'], '-118.2437')

        mock_requests_get.assert_called_once()
        mock_update_or_create.assert_called_once_with(
            name='LOS ANGELES',
            defaults={'latitude': '34.0522', 'longitude': '-118.2437'}
        )

    @patch('TempByLocationApi.service.openmeteo.weather_api')
    def test_get_weather_data_failure(self, mock_weather_api):
        # Test case where the weather API call fails
        mock_weather_api.side_effect = Exception('API error')

        result = LocationService.get_weather_data('34.0522', '-118.2437')

        self.assertIsNone(result)
        mock_weather_api.assert_called_once()


    ##TODO :Add in test to test the weather api call response

if __name__ == '__main__':
    unittest.main()

