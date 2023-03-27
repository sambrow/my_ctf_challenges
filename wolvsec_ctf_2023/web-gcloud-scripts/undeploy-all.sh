#!/bin/bash

while read folder; do
  echo
  echo
  echo -------- PROCESSING: "$folder" ----------------
  ./undeploy-one.sh ../$folder
done <web-chal-folder-list.txt
