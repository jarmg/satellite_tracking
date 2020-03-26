#!/bin/bash

cd frontend
npm run-script build 
cd ../
balena push satellite_imager
