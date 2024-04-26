#!/bin/bash

sudo apt update -y
sudo apt install net-tools -y 
sudo apt install nginx -y
sudo systemctl restart nginx