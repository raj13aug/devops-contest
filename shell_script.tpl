#!/bin/bash

export GCSFUSE_REPO=gcsfuse-`lsb_release -c -s`
echo "deb [signed-by=/usr/share/keyrings/cloud.google.asc] https://packages.cloud.google.com/apt $GCSFUSE_REPO main" | sudo tee /etc/apt/sources.list.d/gcsfuse.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo tee /usr/share/keyrings/cloud.google.asc
sudo apt-get update -y
sleep 20
sudo apt-get install gcsfuse -y
echo ${bucket_name} > test
sudo apt update -y
sleep 20
sudo apt install net-tools -y 
sudo apt install nginx -y
sudo systemctl restart nginx