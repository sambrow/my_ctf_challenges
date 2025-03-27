#!/bin/bash

# common vars
GCLOUD_REGION=us-east5
GCLOUD_PROJECT=web-challenges-453514
GCLOUD_ARTIFACT_REPOSITORY=locker

# app vars
CHAL_NAME=js-puzzle
IMAGE_AND_TAG=$CHAL_NAME:1
GCLOUD_TAG1=$GCLOUD_REGION-docker.pkg.dev/$GCLOUD_PROJECT/$GCLOUD_ARTIFACT_REPOSITORY/$IMAGE_AND_TAG

gcloud builds submit --project=$GCLOUD_PROJECT --tag $GCLOUD_TAG1

gcloud run deploy $CHAL_NAME --image=$GCLOUD_TAG1 --allow-unauthenticated --port=8000 --max-instances=10 --min-instances=1 --min=1 --region=$GCLOUD_REGION --project=$GCLOUD_PROJECT