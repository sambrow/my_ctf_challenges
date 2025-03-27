#!/bin/bash

# common vars
GCLOUD_REGION=us-east5
GCLOUD_PROJECT=web-challenges-453514
GCLOUD_ARTIFACT_REPOSITORY=locker


gcloud run services delete limited-app --region=$GCLOUD_REGION --project=$GCLOUD_PROJECT
