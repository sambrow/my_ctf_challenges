#!/bin/bash

for entry in *; do
    [ -d $entry ] && ./build-one.sh $entry
done
