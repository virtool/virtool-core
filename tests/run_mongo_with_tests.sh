#!/bin/sh
# run tests with mongodb running
if [ "$1" != "--no-pull" ]
then
  sudo docker pull mongo
else
  shift
fi

ID=$(sudo docker run -d --network=host mongo)

tox "$@"

sudo docker stop $ID
sudo docker rm $ID
