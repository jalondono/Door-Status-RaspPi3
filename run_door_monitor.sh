#!/bin/bash -l
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

sleep 60
cd /
cd /home/pi/Documents/Projects/Door-Status-RaspPi3
pwd
source door_env/bin/activate
python3 main.py
