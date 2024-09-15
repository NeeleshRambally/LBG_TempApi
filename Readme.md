pip freeze > requirements.txt  

to run tests:
docker-compose up --build test


to run the app: 
docker-compose up --build


to bring down the entire app : 
docker-compose down



TO RUN TEST : 
docker-compose -f docker-compose.test.yml up --build

TO BRING TEST DOWN: 
docker-compose -f docker-compose.test.yml down
