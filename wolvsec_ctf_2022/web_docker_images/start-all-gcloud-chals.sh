#!/bin/bash

# for each project, apply the yaml that will startup the application in GCP
for entry in *; do
    [ -d $entry ] && ./start-one-gcloud-chal.sh $entry
done
