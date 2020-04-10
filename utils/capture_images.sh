#!/bin/bash

# Source: https://baheyeldin.com/astronomy/using-canon-eos-dslr-cameras-bulb-mode-gphoto2.html

# Number of frames to take
NUMBER=$1

# Exposure, in seconds 
EXPOSURE=$2

# path
IMAGE_PATH=$3
FILE_NAME=$4

mkdir -p $IMAGE_PATH

for COUNT in `seq 1 $NUMBER`
do
  gphoto2 \
  --filename "$FILE_NAME-$COUNT.CR2" \
  --wait-event=1s \
  --set-config eosremoterelease=5 \
  --wait-event=${EXPOSURE}s \
  --set-config eosremoterelease=11 \
  --wait-event-and-download=1s
done
