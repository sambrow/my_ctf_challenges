#!/bin/bash

docker compose build

# common vars
GCLOUD_REGION=us-east5
GCLOUD_PROJECT=wolvctf-2024
GCLOUD_ARTIFACT_REPOSITORY=locker

# app vars
CHAL_NAME=upload-fun
IMAGE_AND_TAG=$CHAL_NAME:1.0
GCLOUD_TAG1=us-east5-docker.pkg.dev/$GCLOUD_PROJECT/$GCLOUD_ARTIFACT_REPOSITORY/$IMAGE_AND_TAG

docker tag $IMAGE_AND_TAG $GCLOUD_TAG1
docker push $GCLOUD_TAG1

# needs --session-affinity to ensure you talk to the instance to which you
# uploaded your file
gcloud run deploy $CHAL_NAME --image=$GCLOUD_TAG1 --allow-unauthenticated --port=80 --min-instances=1 --max-instances=10 --cpu-boost --session-affinity --region=$GCLOUD_REGION --project=$GCLOUD_PROJECT
