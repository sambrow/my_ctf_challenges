#!/bin/bash

# parameter validation
[ -z $1 ] && echo "usage $0 <image:tag>" && exit

IMAGE_AND_TAG=$1

IMAGE=`echo "$1"|grep -o '^[^:]*'`

# This challenge launches Chrome via puppeteer so it needs
# more resources than other ones. Setting concurrency to 20
# because I did stress testing that proves one instance in
# this configuration can handle 20 url posts in parallel.
gcloud run deploy $IMAGE \
--image=us-east5-docker.pkg.dev/wolvsec-ctf-2023-web/locker/$IMAGE_AND_TAG \
--allow-unauthenticated \
--port=8080 \
--concurrency=20 \
--cpu=2 \
--memory=2Gi \
--min-instances=1 \
--max-instances=100 \
--execution-environment=gen2 \
--region=us-east5 \
--project=wolvsec-ctf-2023-web
