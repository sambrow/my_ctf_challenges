#!/bin/bash

docker compose build

# common vars
GCLOUD_REGION=us-east5
GCLOUD_PROJECT=wolvctf-2024
GCLOUD_ARTIFACT_REPOSITORY=locker

# order-up-db
IMAGE_AND_TAG=order-up-db:1.0
GCLOUD_TAG1=us-east5-docker.pkg.dev/$GCLOUD_PROJECT/$GCLOUD_ARTIFACT_REPOSITORY/$IMAGE_AND_TAG

docker tag $IMAGE_AND_TAG $GCLOUD_TAG1
docker push $GCLOUD_TAG1

# order-up-app
IMAGE_AND_TAG=order-up-app:1.0
GCLOUD_TAG2=us-east5-docker.pkg.dev/$GCLOUD_PROJECT/$GCLOUD_ARTIFACT_REPOSITORY/$IMAGE_AND_TAG

docker tag $IMAGE_AND_TAG $GCLOUD_TAG2
docker push $GCLOUD_TAG2

# uncomment the below lines if needed for testing
# during the CTF, order-up instances will be spun up on-demand
# by the service-manager in coordination with the CTFd private_challenges plugin

# start the app
#gcloud run services replace --project=$GCLOUD_PROJECT --region=$GCLOUD_REGION order-up-gcloud-service.yaml
# Can't seem to do this in one command :(
#gcloud run services add-iam-policy-binding order-up-app --project=$GCLOUD_PROJECT --region=$GCLOUD_REGION --member=allUsers  --role=roles/run.invoker


