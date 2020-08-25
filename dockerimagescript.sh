#!/bin/bash

mv Dockerfileclient Dockerfile

docker build . -t client

mv Dockerfile Dockerfileclient

mv Dockerfileserver Dockefile

docker build . -t server

mv Dockerfile Dockerfileserver

docker-compose up & 

echo "docker compose now running, use 
docker exec -it sockets_client_1 /bin/bash
to enter client container in interatactive mode "
