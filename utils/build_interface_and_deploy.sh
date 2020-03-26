#!/bin/bash

cd frontend
npm build 
cd ../
balena push satellite_imager
