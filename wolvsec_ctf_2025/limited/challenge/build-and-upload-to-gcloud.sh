#!/bin/bash

# docker compose build

# common vars
GCLOUD_REGION=us-east5
GCLOUD_PROJECT=web-challenges-453514
GCLOUD_ARTIFACT_REPOSITORY=locker

# limited-db
IMAGE_AND_TAG=limited-db:1.0
GCLOUD_TAG1=us-east5-docker.pkg.dev/$GCLOUD_PROJECT/$GCLOUD_ARTIFACT_REPOSITORY/$IMAGE_AND_TAG

gcloud builds submit --project=$GCLOUD_PROJECT --tag $GCLOUD_TAG1 ./db

# docker tag $IMAGE_AND_TAG $GCLOUD_TAG1
# docker push $GCLOUD_TAG1

# limited-app
IMAGE_AND_TAG=limited-app:1.0
GCLOUD_TAG2=us-east5-docker.pkg.dev/$GCLOUD_PROJECT/$GCLOUD_ARTIFACT_REPOSITORY/$IMAGE_AND_TAG

gcloud builds submit --project=$GCLOUD_PROJECT --tag $GCLOUD_TAG2 ./app

# docker tag $IMAGE_AND_TAG $GCLOUD_TAG2
# docker push $GCLOUD_TAG2

# start the app
export GCLOUD_TAG1
export GCLOUD_TAG2
envsubst < limited-gcloud-service.yaml > limited-gcloud-service-substituted.yaml

gcloud run services delete limited-app --quiet --region=us-east5 --project=$GCLOUD_PROJECT

gcloud run services replace --project=$GCLOUD_PROJECT --region=$GCLOUD_REGION limited-gcloud-service-substituted.yaml
# Can't seem to do this in one command :(
gcloud run services add-iam-policy-binding limited-app --project=$GCLOUD_PROJECT --region=$GCLOUD_REGION --member=allUsers  --role=roles/run.invoker