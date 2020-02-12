#!/bin/bash

# Source: https://baheyeldin.com/astronomy/using-canon-eos-dslr-cameras-bulb-mode-gphoto2.html

# Number of frames to take
NUMBER=$1

# Exposure, in seconds 
EXPOSURE=$2

# path
IMAGE_PATH=$3

mkdir $IMAGE_PATH
cd $IMAGE_PATH

for COUNT in `seq 1 $NUMBER`
do
  gphoto2 \
  --filename "%y%m%d-%H%M%S-$COUNT.CR2" \
  --wait-event=2s \
  --set-config eosremoterelease=5 \
  --wait-event=${EXPOSURE}s \
  --set-config eosremoterelease=11 \
  --wait-event-and-download=1s
done
