#!/bin/bash

# build the docker image using docker compose so
# docker-compose.yml can control the image name:tag
docker compose -f challenge/docker-compose.yml build

# Source will not be provided for this challenge.