import requests
import logging
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

from django.conf import settings
from .models import Location

logger = logging.getLogger(__name__)

# Setup caching and retry for the Open-Meteo API client
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)


class LocationService:

    @staticmethod
    def fetch_and_save_location_coordinates(location):
        """
        Fetches the latitude and longitude coordinates for a given location.
        If the location already exists in the database, returns the stored coordinates.
        Otherwise, fetches the coordinates using the Nominatim API and saves the result to the database.

        Args:
            location (str): The name of the location to query.

        Returns:
            dict: A dictionary containing 'location', 'latitude', and 'longitude' if successful.
            None: If no results are found or the API call fails.
        """
        location_upper = location.upper()

        # Check if the location is already in the database - this saves api calls in the long run
        try:
            location_obj = Location.objects.get(name=location_upper)
            logger.info(f"Location found in database: {location_upper}")

            return {
                'location': location_upper,
                'latitude': location_obj.latitude,
                'longitude': location_obj.longitude
            }
        except Location.DoesNotExist:
            # If the location is not found in the database, proceed to fetch from API
            logger.info(f"Location not found in database. Fetching from API: {location_upper}")

        # Proceed with fetching from the API
        query = location_upper.replace(' ', '+')
        url = f"{settings.NOMINATIM_API_URL}?q={query}&format=json"

        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; MyApp/1.0; +https://example.com)'
        }

        try:
            response = requests.get(url, headers=headers)
            logger.debug(f"API Request URL: {url}")
            logger.debug(f"API Response Status Code: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                logger.debug(f"API Response Data: {data}")

                if data:
                    latitude = data[0]['lat']
                    longitude = data[0]['lon']

                    # Save location to database with the name in uppercase
                    location_obj, created = Location.objects.update_or_create(
                        name=location_upper,
                        defaults={'latitude': latitude, 'longitude': longitude}
                    )

                    if created:
                        logger.info(f"Created new location: {location_upper}")
                    else:
                        logger.info(f"Updated existing location: {location_upper}")

                    return {
                        'location': location_upper,
                        'latitude': latitude,
                        'longitude': longitude
                    }
                else:
                    logger.warning("No results found for the given location.")
                    return None
            else:
                logger.error("Failed to connect to the API.")
                return None

        except Exception as e:
            logger.exception(f"An error occurred while fetching and saving coordinates: {e}")
            return None


    @staticmethod
    def get_weather_data(latitude, longitude):
        """
        Fetches the weather data for a given latitude and longitude from the Open-Meteo API.

        Args:
            latitude (str): The latitude of the location.
            longitude (str): The longitude of the location.

        Returns:
            dict: A dictionary containing weather data.
            None: If the API call fails.
        """
        try:
            # Prepare the parameters for the Open-Meteo API call
            params = {
                "latitude": float(latitude),
                "longitude": float(longitude),
                "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"]
            }

            responses = openmeteo.weather_api(url="https://api.open-meteo.com/v1/forecast", params=params)
            response = responses[0]

            logger.debug(f"Weather API Response Data: {response}")

            # Extract the weather data into a pandas DataFrame
            daily = response.Daily()
            daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
            daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
            daily_precipitation_sum = daily.Variables(2).ValuesAsNumpy()


            daily_data = {
                "date": pd.date_range(
                    start=pd.to_datetime(daily.Time(), unit="s", utc=True),
                    end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
                    freq=pd.Timedelta(seconds=daily.Interval()),
                    inclusive="left"
                ),
                "temperature_2m_max": daily_temperature_2m_max,
                "temperature_2m_min": daily_temperature_2m_min,
                "precipitation_sum": daily_precipitation_sum
            }

            daily_dataframe = pd.DataFrame(data=daily_data)
            logger.debug(f"Daily Weather Data DataFrame: {daily_dataframe}")

            return daily_dataframe.to_dict(orient='records')
        except Exception as e:
            logger.exception(f"An error occurred while fetching weather data: {e}")
            return None