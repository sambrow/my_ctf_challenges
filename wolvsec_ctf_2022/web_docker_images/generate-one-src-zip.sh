#!/bin/bash

# run this to generate a zip file that should be downloadable from the challenge page

# parameter validation
[ -z $1 ] && echo "usage $0 <dir>" && exit
[ ! -d $1 ] && echo "no such directory: $1" &&  exit

source ./set-shared-vars.sh

CHAL_NUM=$1

cd $CHAL_NUM

# copy the source
rm -rf ../src
mkdir ../src
cp -r ./* ../src

# remove files we don't want included
rm -rf ../src/challengeApp/target
rm -rf ../src/node_modules
rm ../src/readme.txt
rm ../src/solve.txt
rm ../src/src.zip
rm ../src/start-this-gcloud-chal.sh
find ../src -type f -name '.DS_Store' -delete

# redact the flag from the copied source
# -i '' means replace inline with no backup file created
sed -i '' 's/wsc{.*}/wsc{redacted}/' ../src/Dockerfile
sed -i '' 's/PASSWORD=.*$/PASSWORD=redacted/' ../src/Dockerfile
[ -f ../src/flag.txt ] && grep -q 'wsc{' ../src/flag.txt && echo 'wsc{redacted}' > ../src/flag.txt
[ -f ../src/flag.txt ] && grep -qv 'wsc{' ../src/flag.txt && echo 'redacted' > ../src/flag.txt

# zip it up
rm src.zip
cd ..
zip -r src.zip src
cd -
mv ../src.zip .

# remove the source folder
rm -rf ../src

cd ..