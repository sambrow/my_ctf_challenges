#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

while read FOLDER; do
  echo
  echo
  echo -------- PROCESSING: "$FOLDER" ----------------
  $SCRIPT_DIR/deploy-one.sh $SCRIPT_DIR/../$FOLDER
done <$SCRIPT_DIR/web-chal-FOLDER-list.txt
