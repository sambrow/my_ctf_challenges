#!/bin/bash

# parameter validation
[ -z $1 ] && echo "usage $0 <dir>" && exit
[ ! -d $1 ] && echo "no such directory: $1" &&  exit

source ./set-shared-vars.sh

CHAL_NUM=$1
cd $CHAL_NUM

# grabs the image name from docker-compose.yml
# image: wsc-2022-web-3:2 --> wsc-2022-web-3
export IMAGE=`grep image: docker-compose.yml | grep -o '[^ :]*:[^:]*$' | grep -o '^[^:]*'`

# grabs the image name:tag from docker-compose.yml
# image: wsc-2022-web-3:2 --> wsc-2022-web-3:2
export IMAGE_AND_TAG=`grep 'image:' docker-compose.yml |grep -o '[^: ]*:[^:]*$'`

# let the chal control the rest
./start-this-gcloud-chal.sh
