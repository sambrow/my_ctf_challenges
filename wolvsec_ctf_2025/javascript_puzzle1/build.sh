# build the docker images locally as a sanity check
docker compose -f challenge/docker-compose.yml build || exit 1

# create the dist.tar.gz source we make available to contestants
rm -rf _dist_
mkdir -p _dist_

rm -rf challenge/node_modules

cp -r challenge/* _dist_

# remove deploy scripts
rm _dist_/*.sh

# swap out real flag with a fake
rm _dist_/flag.txt
printf '%s' 'wctf{flag-placeholder}' > _dist_/flag.txt

rm dist.tar.gz
tar -czvf dist.tar.gz -C _dist_ .

rm -rf _dist_

echo ""
echo "created challenge source"
ls -la dist.tar.gz
