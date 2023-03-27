#!/bin/bash

# parameter validation
[ -z $1 ] && echo "usage $0 <dir>" && exit
[ ! -d $1 ] && echo "no such directory: $1" &&  exit

source ./set-shared-vars.sh

CHAL_NUM=$1

cd $CHAL_NUM

# grabs the image name:tag from docker-compose.yml
# image: wsc-2022-web-3:2 --> wsc-2022-web-3:2
IMAGE_AND_TAG=`grep 'image:' docker-compose.yml |grep -o '[^: ]*:[^:]*$'`

docker tag $IMAGE_AND_TAG gcr.io/$GCP_PROJECT/$IMAGE_AND_TAG
docker push gcr.io/$GCP_PROJECT/$IMAGE_AND_TAG
