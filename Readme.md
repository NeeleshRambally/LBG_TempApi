
# Project Overview

This project consists of two APIs:

1. **Location API**: Retrieves the latitude and longitude for a given location.
2. **Weather Forecast API**: Provides the weather forecast for the week for a given location, including its latitude and longitude.

## Requirements

To install the necessary dependencies, run:

pip install -r requirements.txt

## Running the Project

### Running the Application

To build and run the application using Docker Compose:

docker-compose up --build

To bring down the application:

docker-compose down

### Running Tests

python manage.py test --settings=TempApi.test_settings

## Additional Commands

- To update the dependencies, run:

pip freeze > requirements.txt

## Notes

- Ensure Docker and Docker Compose are installed on your machine to run the commands above.
- The APIs use environment variables for configuration; ensure you have set up a `.env` file as required.
- The tests are designed to verify both APIs' functionality and their integration.

## CI/CD : 
The project uses a Continuous Integration (CI) pipeline defined in GitHub Actions to automate testing and building processes. The pipeline is triggered on every push or pull request to the main branch. It consists of two jobs:

Test Job: This job runs unit tests to ensure code quality. It sets up a Python environment, installs all necessary dependencies from requirements.txt, and executes the tests using Django's test runner (python manage.py test --settings=TempApi.test_settings). This job helps ensure that any new changes do not introduce bugs or break existing functionality.

Docker Build Job: This job builds Docker images for the application using Docker Compose. It sets up Docker, installs Docker Compose, and utilizes cached Docker layers to speed up the build process. This job ensures that the application can be packaged and deployed consistently in any environment that supports Docker.

Together, these jobs ensure that the application is continuously tested and built, maintaining high quality and readiness for deployment.