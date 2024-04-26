#!/bin/bash

export GCSFUSE_REPO=gcsfuse-`lsb_release -c -s`
echo "deb [signed-by=/usr/share/keyrings/cloud.google.asc] https://packages.cloud.google.com/apt $GCSFUSE_REPO main" | sudo tee /etc/apt/sources.list.d/gcsfuse.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo tee /usr/share/keyrings/cloud.google.asc
sudo apt-get update -y
sleep 20
sudo apt-get install gcsfuse -y
sleep 15
mkdir -p gcs-bucket  
sudo chown -R 777 gcs-bucket
sudo echo artifact-bucket-x1n1l5ev > testing.txt
sudo gcsfuse -o allow_other -file-mode=777 -dir-mode=777 artifact-bucket-x1n1l5ev gcs-bucket > out.txt
sleep 10
sudo touch gcs-bucket/cloudroot7.txt
echo ${bucket_name} > test
sudo apt install net-tools -y
sudo apt install python3-pip -y
sudo pip install requests ansicolors -y
sudo apt install nginx -y
sudo systemctl restart nginx