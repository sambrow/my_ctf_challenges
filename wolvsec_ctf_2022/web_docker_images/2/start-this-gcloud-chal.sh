#!/bin/bash

# assumes these are set by the caller
[ -z $GCP_PROJECT ] && echo GCP_PROJECT must be defined && exit
[ -z $GCP_REGION ] && echo GCP_REGION must be defined && exit
[ -z $IMAGE ] && echo IMAGE must be defined && exit
[ -z $IMAGE_AND_TAG ] && echo IMAGE_AND_TAG must be defined && exit

# Some requests in this chal can launch an embedded Chrome browser
# using puppeteer.  These settings have been tuned accordingly.
#
# Using gen2 because it should be faster but also to avoid the logs getting spammed
# by these:
#
# Container Sandbox: Unsupported syscall setsockopt(0xb,0x6,0x9,0x3ee1608589cc,0x4,0x29910fc86500).
# It is very likely that you can safely ignore this message and that this is not the cause of any error you might be
# troubleshooting. Please, refer to https://gvisor.dev/c/linux/amd64/setsockopt for more information.
#
gcloud beta run deploy $IMAGE \
--image=gcr.io/$GCP_PROJECT/$IMAGE_AND_TAG \
--allow-unauthenticated \
--port=80 \
--concurrency=10 \
--cpu=4 \
--memory=8192Mi \
--min-instances=1 \
--max-instances=100 \
--no-use-http2 \
--cpu-throttling \
--execution-environment=gen2 \
--platform=managed \
--region=$GCP_REGION \
--project=$GCP_PROJECT
