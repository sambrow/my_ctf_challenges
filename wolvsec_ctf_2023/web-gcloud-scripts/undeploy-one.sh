#!/bin/bash

# parameter validation
[ -z $1 ] && echo "usage $0 <dir>" && exit

folder=$1
[ ! -d $folder ] && echo "no such directory: $folder" &&  exit

# grabs the image name from docker-compose.yml
# image: zombie-101:1 --> zombie-101
IMAGE=`grep image: $folder/docker-compose.yml | grep -o '[^ :]*:[^:]*$' | grep -o '^[^:]*'`

gcloud run services delete $IMAGE --region=us-east5 --project=wolvsec-ctf-2023-web -q &> /dev/null
