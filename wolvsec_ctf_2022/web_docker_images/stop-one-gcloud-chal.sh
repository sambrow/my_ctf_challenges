#!/bin/bash

# parameter validation
[ -z $1 ] && echo "usage $0 <dir>" && exit
[ ! -d $1 ] && echo "no such directory: $1" &&  exit

source ./set-shared-vars.sh

CHAL_NUM=$1
cd $CHAL_NUM

# grabs the image name from docker-compose.yml
# image: wsc-2022-web-3:2 --> wsc-2022-web-3
IMAGE=`grep image: docker-compose.yml | grep -o '[^ :]*:[^:]*$' | grep -o '^[^:]*'`

gcloud run services delete $IMAGE -q --region=$GCP_REGION --project=$GCP_PROJECT
