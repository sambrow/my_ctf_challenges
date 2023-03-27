#!/bin/bash

# parameter validation
[ -z $1 ] && echo "usage $0 <dir>" && exit
[ ! -d $1 ] && echo "no such directory: $1" &&  exit

CHAL_NUM=$1
cd $CHAL_NUM

# grabs the image name from docker-compose.yml
# image: wsc-2022-web-3:2 --> wsc-2022-web-3
export IMAGE=`grep image: docker-compose.yml | grep -o '[^ :]*:[^:]*$' | grep -o '^[^:]*'`

# grabs the image tag from docker-compose.yml
# image: wsc-2022-web-3:2 --> 2
TAG=`grep image: docker-compose.yml | grep -o '[^:]*$'`
NEWTAG=$((TAG+1))

# Incrementing the image tag will ensure that, when we push to gcloud, we don't
# accidentally use the previous image.

# -i '' means replace inline with no backup file created
sed -i '' "s/image: .*$/image: $IMAGE:$NEWTAG/" docker-compose.yml

cd ..
