#!/bin/bash

# parameter validation
[ -z $1 ] && echo "usage $0 <dir>" && exit

FOLDER=$1
[ ! -d $FOLDER ] && echo "no such directory: $FOLDER" &&  exit

docker compose -f $FOLDER/docker-compose.yml build

# grabs the image name:tag from docker-compose.yml
# image: zombie-101:1 --> zombie-101:1
IMAGE_AND_TAG=`grep 'image:' $FOLDER/docker-compose.yml |grep -o '[^: ]*:[^:]*$'`

GCLOUD_TAG=us-east5-docker.pkg.dev/wolvsec-ctf-2023-web/locker/$IMAGE_AND_TAG

docker tag $IMAGE_AND_TAG $GCLOUD_TAG

docker push $GCLOUD_TAG
