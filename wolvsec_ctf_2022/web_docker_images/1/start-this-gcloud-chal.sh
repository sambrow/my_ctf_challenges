#!/bin/bash

# assumes these are set by the caller
[ -z $GCP_PROJECT ] && echo GCP_PROJECT must be defined && exit
[ -z $GCP_REGION ] && echo GCP_REGION must be defined && exit
[ -z $IMAGE ] && echo IMAGE must be defined && exit
[ -z $IMAGE_AND_TAG ] && echo IMAGE_AND_TAG must be defined && exit

# This chal has low resource needs so can get by with the default low cpu/mem.

gcloud run deploy $IMAGE \
--image=gcr.io/$GCP_PROJECT/$IMAGE_AND_TAG \
--allow-unauthenticated \
--port=80 \
--min-instances=1 \
--max-instances=100 \
--no-use-http2 \
--cpu-throttling \
--platform=managed \
--region=$GCP_REGION \
--project=$GCP_PROJECT
