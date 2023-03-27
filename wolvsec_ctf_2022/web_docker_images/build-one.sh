#!/bin/bash

# parameter validation
[ -z $1 ] && echo "usage $0 <dir>" && exit
[ ! -d $1 ] && echo "no such directory: $1" &&  exit

# generate the src.zip (flag will be redacted)
./generate-one-src-zip.sh $1

# build the docker image so it exists locally
# we increment the image tag to ensure gcloud runs the latest content
./increment-one-image-tag.sh $1
docker-compose -f $1/docker-compose.yml build

# tag and push its docker image to Google Container Registry
# this will take a few mins the first time but later runs will be faster
./tag-and-push-one-docker-image.sh $1
