
# Project Description
This project provides a comprehensive API service that fetches and manages weather data for a specified location. The application integrates with external services to retrieve geographical coordinates and weather forecasts, storing relevant data in a database for future reference. The main features include:

Fetch Latitude and Longitude of a Location: The API takes a user-provided location name (such as a city or town) and retrieves its latitude and longitude coordinates using a reliable external service. This information is essential for obtaining accurate weather forecasts.

Retrieve a 7-Day Weather Forecast: Using the latitude and longitude obtained, the API queries the Open-Meteo weather service to fetch a detailed 7-day weather forecast. The forecast includes:

Daily High and Low Temperatures: Maximum and minimum temperatures expected for each day.
Probability of Rain: The likelihood of precipitation for each of the upcoming seven days.
Save and Reuse Location Data: The latitude and longitude of the queried locations are stored in a database, reducing the need for redundant API calls and ensuring quick response times. Whenever a request is made for a previously searched location, the system uses the stored coordinates to fetch the weather forecast, optimizing performance.

API-Driven Architecture: The application is designed using RESTful principles, providing a clean and simple interface for interacting with location and weather data. Users can easily make requests to retrieve coordinates, obtain weather forecasts, and interact with the stored data.

# Project Overview

This project consists of two APIs:

1. **Location API**: Retrieves the latitude and longitude for a given location.
2. **Weather Forecast API**: Provides the weather forecast for the week for a given location, including its latitude and longitude.

## Requirements

To install the necessary dependencies, run:

**pip install -r requirements.txt**


## Running the Project

### Running the Application

To build and run the application using Docker Compose:

**docker-compose up --build**

- Testing the api locally using POSTMAN or another API testing tool
use URL : http://localhost:8000/api/get-weather/?location=Munich
- you can enter any location as a query parameter 

To stop the application:

**docker-compose down**

### Running Tests
unit test use its own config file hence this is passed in as an argument

**python manage.py test --settings=TempApi.test_settings**

## Additional Commands

- To update the dependencies, run:

pip freeze > requirements.txt

## Notes

- Ensure Docker and Docker Compose are installed on your machine to run the commands above.
- The tests are designed to verify both APIs' functionality and their integration.

## CI/CD : 
The project uses a Continuous Integration (CI) pipeline defined in GitHub Actions to automate testing and building processes. The pipeline is triggered on every push or pull request to the main branch. It consists of two jobs:

Test Job: This job runs unit tests to ensure code quality. It sets up a Python environment, installs all necessary dependencies from requirements.txt, and executes the tests using Django's test runner (python manage.py test --settings=TempApi.test_settings). This job helps ensure that any new changes do not introduce bugs or break existing functionality.

Docker Build Job: This job builds Docker images for the application using Docker Compose. It sets up Docker, installs Docker Compose, and utilizes cached Docker layers to speed up the build process. This job ensures that the application can be packaged and deployed consistently in any environment that supports Docker.

Together, these jobs ensure that the application is continuously tested and built, maintaining high quality and readiness for deployment.


## Deliverables
### Time Taken to Complete
The entire project, including the setup of a CI/CD pipeline, was completed in approximately 2.5 hours.

### Thought Process
Before diving into the project, I spent a few minutes planning the overall approach to building the API. This planning phase involved:
- Brainstorming the external APIs to use
- Designing the database schema
- Structuring the API endpoints
- Defining the overall application architecture
- To simplify development and avoid creating a separate PostgreSQL instance, I opted to use a Docker image of PostgreSQL for local connection. This allowed me to connect and persist data to the database while setting up the data layer. The application can be easily extended to connect to an external PostgreSQL database instance in the future.
- My goal was to run the application with a single command, so I used Docker Compose to orchestrate both the database and the application startup. This approach ensures that the database is created, the required tables are initialized, and all migrations are run automatically when the application is started.
- I automated the testing using GitHub Actions that run all the unit tests as described above

### Key Decisions
- I chose 'https://open-meteo.com/' as the weather data provider because it offers a 7-day forecast (including high/low temperatures and probability of rain) for a given location.
- For retrieving location data (latitude and longitude), I used the 'https://nominatim.openstreetmap.org' API, which accepts a search phrase and returns the corresponding coordinates if found.
- To optimize performance, I store the latitude and longitude values in the database, allowing for quick lookups and reuse in subsequent weather data requests.
### Limitations
- The database is ephemeral and gets destroyed when the application is stopped, resulting in the loss of saved location data. This behavior was anticipated since the app was designed to run locally.
- The location API used could be more comprehensive and accurate. In this example, a free API was chosen, which may not cover all known locations in detail.
### Wishlist
- Additional unit tests to cover more scenarios. Currently, only three test cases are included, but the test coverage could be significantly expanded.
- Implement caching using Redis or another caching mechanism to improve performance.