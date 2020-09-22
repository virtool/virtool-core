#!/bin/sh
# run tests with mongodb running
docker pull mongo
ID=`docker run -d --network=host mongo`

pytest .

docker stop $ID
docker rm $ID