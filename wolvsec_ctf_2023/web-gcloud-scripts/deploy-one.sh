#!/bin/bash

# parameter validation
[ -z $1 ] && echo "usage $0 <dir>" && exit

FOLDER=$1
[ ! -d $FOLDER ] && echo "no such directory: $FOLDER" &&  exit


# grabs the image name from docker-compose.yml
# image: zombie-101:1 --> zombie-101
IMAGE=`grep image: $FOLDER/docker-compose.yml | grep -o '[^ :]*:[^:]*$' | grep -o '^[^:]*'`

# grabs the image name:tag from docker-compose.yml
# image: zombie-101:1 --> zombie-101:1
IMAGE_AND_TAG=`grep 'image:' $FOLDER/docker-compose.yml |grep -o '[^: ]*:[^:]*$'`

DEPLOY_SCRIPT=./deploy-scripts/deploy-$IMAGE.sh

[ ! -f $DEPLOY_SCRIPT ] && echo "no such file: $DEPLOY_SCRIPT" && exit

$DEPLOY_SCRIPT $IMAGE_AND_TAG

