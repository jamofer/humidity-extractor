#!/bin/bash

if [ -z "$1" ]
  then
    echo "Usage:"
    echo "  ./install.sh [product] # [default | solid state]"
    exit
fi


function ok {
  echo ✅
}

function no {
  echo ❌
}

WORKSPACE=$(cd `dirname $0` && pwd)
product="$1"

SERVICE="humidity-extractor.service"

SERVICE_CONTENT="[Unit]\n
Description=Humidity extractor\\n
After=network.target\n
\n
[Service]\n
User=pi\n
WorkingDirectory=$WORKSPACE\n
ExecStart=$WORKSPACE/main.py\n
Restart=always\n
\n
[Install]\n
WantedBy=multi-user.target\n
"

echo -n [ Bootstrap environment ...............................
type pip 2>&1 > /dev/null || sudo apt-get install python-pip > /dev/null &&
sudo systemctl stop $SERVICE  2>&1 > /dev/null || echo /dev/null &&
mkdir -p $WORKSPACE/public  > /dev/null && ok || no
echo -n [ Installing dependencies .............................
#pip install -r $WORKSPACE/requirements.txt --ignore-installed && ok || no
echo -n [ Setup backend .......................................
sudo echo -e $SERVICE_CONTENT | sudo tee /lib/systemd/system/$SERVICE &&
sudo systemctl enable $SERVICE > /dev/null && ok || no
echo -n [ Starting backend ....................................
$WORKSPACE/main.py -p $product &&
sudo systemctl start $SERVICE > /dev/null && ok || no
