#!/bin/bash

docker rm -f kafka &> /dev/null
docker run -itd -p 2181:2181 -p 9092:9092 --env ADVERTISED_HOST=`docker-machine ip \`docker-machine active\`` --env ADVERTISED_PORT=9092 -m 4G --name kafka wolf_data_router
