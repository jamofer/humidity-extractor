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

WORKSPACE="/home/pi/humidity-extractor"
host="$1"
product="$2"

echo -n [ Bootstrap environment ...............................
yarn --cwd front build > /dev/null 2>&1 &&
ssh pi@$host "sudo systemctl stop $SERVICE"  2>&1 > /dev/null || echo > /dev/null &&
ssh pi@$host "mkdir -p $WORKSPACE/public"  > /dev/null && ok || no
echo -n [ Deploying frontend ..................................
scp -r front/build/* pi@$host:$WORKSPACE/public/ > /dev/null && ok || no
echo -n [ Deploying backend ...................................
scp *.sh *.py *.txt pi@$host:$WORKSPACE/. > /dev/null && ok || no
ssh pi@$host "$WORKSPACE/install.sh $product"
