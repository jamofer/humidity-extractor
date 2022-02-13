#!/bin/bash

if [ -z "$2" ]
  then
    echo "Usage:"
    echo "  ./deploy.sh [HOST] [PRODUCT]"
    exit
fi

function ok {
  echo ✅
}

function no {
  echo ❌
}

SERVICE="humidity-extractor.service"
WORKSPACE="/home/pi/humidity-extractor"
host="$1"
product="$2"

echo -n [ Bootstrap environment ...............................
yarn --cwd front build > /dev/null 2>&1 &&
ssh pi@$host "type pip || sudo apt-get install python-pip" > /dev/null &&
ssh pi@$host "sudo systemctl stop $SERVICE"  > /dev/null &&
ssh pi@$host "mkdir -p $WORKSPACE/public"  > /dev/null && ok || no
echo -n [ Deploying frontend ..................................
scp -r front/build/* pi@$host:$WORKSPACE/public/ > /dev/null && ok || no
echo -n [ Deploying backend ...................................
scp *.py *.txt *.service pi@$host:$WORKSPACE/. > /dev/null && ok || no
echo -n [ Installing dependencies .............................
ssh pi@$host "pip install -r $WORKSPACE/requirements.txt" > /dev/null && ok || no
echo -n [ Setup backend .......................................
ssh pi@$host "sudo cp $WORKSPACE/$SERVICE /lib/systemd/system/." > /dev/null &&
ssh pi@$host "sudo systemctl enable $SERVICE" > /dev/null && ok || no
echo -n [ Starting backend ....................................
/home/pi/humidity-extractor/main.py -p $product &&
ssh pi@$host "sudo systemctl start $SERVICE" > /dev/null && ok || no
