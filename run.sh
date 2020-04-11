#!/bin/bash

export ROOT_DIR=/home/jared/satellite_imager/
export PYTHONPATH=${ROOT_DIR}src
export IMAGE_OUTPUT_DIR=${ROOT_DIR}server/static/observations
export HEALTH_DIR=${ROOT_DIR}.health
export EXPOSURE=5
export MOUNT_IP=ESP_6DAE10.home

cd $ROOT_DIR

source ${ROOT_DIR}/utils/start_mount_health_checker.sh $MOUNT_IP > /dev/null &

sudo EXPOSURE=$EXPOSURE PYTHONPATH=$PYTHONPATH ROOT_DIR=$ROOT_DIR IMAGE_OUTPUT_DIR=$IMAGE_OUTPUT_DIR HEALTH_DIR=$HEALTH_DIR python3.5 /home/jared/satellite_imager/server/main.py

EXIT
