#!/bin/bash

# for each project, delete the yaml so the apps will all shut down
for entry in *; do
    [ -d $entry ] && ./stop-one-gcloud-chal.sh $entry
done
