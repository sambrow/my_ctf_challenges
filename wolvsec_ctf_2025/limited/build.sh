#!/bin/bash

# build the docker images locally as a sanity check
docker compose -f challenge/docker-compose.yml build || exit 1

# create the dist.tar.gz source we make available to contestants

rm -rf _dist_
mkdir -p _dist_

cp -r challenge/* _dist_

# remove unwanted files
rm _dist_/*.yaml
rm _dist_/*.sh

# redact the flags

# NOTE: Using perl instead of sed since sed -i works differently
# on OSX vs linux/WSL :(
perl --version > /dev/null || (echo "perl is required" &&  exit)

perl -pi -e s/maricrissarah/REDACTED_FLAG/g _dist_/db/initialize/initialize.sql
perl -pi -e s/Flag_843423739/Flag_REDACTED/g _dist_/db/initialize/initialize.sql
perl -pi -e s/wctf{[^}]+}/wctf{redacted-flag}/g _dist_/db/initialize/initialize.sql

perl -pi -e s/wctf{[^}]+}/wctf{redacted-flag}/g _dist_/app/app.py

rm dist.tar.gz
tar -czvf dist.tar.gz -C _dist_ .

rm -rf _dist_

echo ""
echo "created challenge source"
ls -la dist.tar.gz
