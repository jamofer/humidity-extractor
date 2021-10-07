#!/bin/bash

if [ -z "$1" ]
  then
    echo "Usage:"
    echo "  ./deploy.sh [HOST]"
fi

SERVICE="humidity-extractor.service"
WORKSPACE="/home/pi/humidity-extractor"
host="$1"

ssh pi@$host "sudo systemctl stop $SERVICE"
ssh pi@$host "mkdir -t $WORKSPACE"
scp -r !(venv*) pi@$host:~/humidity-extractor/.
ssh pi@$host "pip install -r $WORKSPACE/requirements.txt"
ssh pi@$host "sudo cp $WORKSPACE/$SERVICE /lib/systemd/system/."
ssh pi@$host "sudo systemctl enable $SERVICE"
ssh pi@$host "sudo systemctl start $SERVICE"
