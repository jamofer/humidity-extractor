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

read -d '' SERVICE_CONTENT << EOF
[Unit]\n
Description=Humidity extractor\n
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
EOF

echo -n [ Bootstrap environment ...............................
type npm 2>&1 > /dev/null || curl -sL https://deb.nodesource.com/setup_12.x | sudo bash - &&
type npm 2>&1 > /dev/null || sudo apt install nodejs &&
type npm 2>&1 > /dev/null || npm install --global yarn &&
yarn --cwd front build > /dev/null 2>&1 &&
type pip 2>&1 > /dev/null || sudo apt-get install python-pip > /dev/null &&
sudo systemctl stop $SERVICE  > /dev/null &&
mkdir -p $WORKSPACE/public  > /dev/null && ok || no
echo -n [ Deploying frontend ..................................
cp -r $WORKSPACE/front/build/* $WORKSPACE/public/ > /dev/null && ok || no
echo -n [ Installing dependencies .............................
pip install -r $WORKSPACE/requirements.txt > /dev/null && ok || no
echo -n [ Setup backend .......................................
sudo echo -e $SERVICE_CONTENT /lib/systemd/system/$SERVICE > /dev/null &&
sudo systemctl enable $SERVICE > /dev/null && ok || no
echo -n [ Starting backend ....................................
$WORKSPACE/main.py -p $product &&
sudo systemctl start $SERVICE > /dev/null && ok || no
