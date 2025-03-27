#!/bin/bash

# common vars
GCLOUD_REGION=us-east5
GCLOUD_PROJECT=web-challenges-453514
# GCLOUD_PROJECT=vocal-tracer-453900-j6
GCLOUD_ARTIFACT_REPOSITORY=locker

# app vars
CHAL_NAME=beginner-jwt-learning
IMAGE_AND_TAG=$CHAL_NAME:1.0
GCLOUD_TAG1=us-east5-docker.pkg.dev/$GCLOUD_PROJECT/$GCLOUD_ARTIFACT_REPOSITORY/$IMAGE_AND_TAG

gcloud builds submit --project=$GCLOUD_PROJECT --tag $GCLOUD_TAG1

gcloud run deploy $CHAL_NAME --image=$GCLOUD_TAG1 --allow-unauthenticated --port=3000 --max-instances=10 --min-instances=1 --min=1 --concurrency=60 --memory=1Gi --cpu-boost --region=$GCLOUD_REGION --project=$GCLOUD_PROJECT