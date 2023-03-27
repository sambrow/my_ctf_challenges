#!/bin/bash

# parameter validation
[ -z $1 ] && echo "usage $0 <image:tag>" && exit

IMAGE_AND_TAG=$1

IMAGE=`echo "$1"|grep -o '^[^:]*'`

# optional port override (default is 80)
PORT=$2
[ -z $PORT ] && PORT=80

gcloud run deploy $IMAGE \
--image=us-east5-docker.pkg.dev/wolvsec-ctf-2023-web/locker/$IMAGE_AND_TAG \
--allow-unauthenticated \
--port=$PORT \
--concurrency=30 \
--cpu=1 \
--memory=512Mi \
--min-instances=1 \
--max-instances=100 \
--execution-environment=gen1 \
--region=us-east5 \
--project=wolvsec-ctf-2023-web
