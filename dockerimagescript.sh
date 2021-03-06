#!/bin/bash

mv Dockerfileclient Dockerfile

docker build . -t client

mv Dockerfile Dockerfileclient

mv Dockerfileserver Dockerfile

docker build . -t server

mv Dockerfile Dockerfileserver

export UID
export GID=$(id -g)

docker-compose up -d

echo "docker compose now running, use 
docker exec -it sockets_client_1 /bin/bash
to enter client container in interatactive mode "
