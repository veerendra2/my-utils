#!/usr/bin/env bash

if [ "$1" == "" ]; then
    COUNT=1
else
    COUNT=$1
fi

for x in $(eval echo {1..$COUNT}); do
 dockerid=`sudo docker run -d my-website`
 dockerip=`sudo docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $dockerid`
 echo "http://$dockerip:80"
done
