#! /bin/bash

./generate-one-src-zip.sh hidden-css
./generate-one-src-zip.sh filter-madness
./generate-one-src-zip.sh zombie-101 zombie-common
./generate-one-src-zip.sh zombie-201 zombie-common
./generate-one-src-zip.sh zombie-301 zombie-common
./generate-one-src-zip.sh zombie-401 zombie-common

ls -la target
