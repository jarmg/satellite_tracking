#!/bin/bash 


# Source: https://pimylifeup.com/raspberry-pi-dslr-camera-control/

git clone https://github.com/gphoto/libgphoto2.git

cd libgphoto2
autoreconf --install --symlink
./configure
make
make install

cd ../
git clone https://github.com/gphoto/gphoto2.git

cd gphoto2
autoreconf --install --symlink
./configure
make
make install

ldconfig

/usr/local/lib/libgphoto2/print-camera-list udev-rules version 201 group plugdev mode 0660 | tee /etc/udev/rules.d/90-libgphoto2.rules
/usr/local/lib/libgphoto2/print-camera-list hwdb | tee /etc/udev/hwdb.d/20-gphoto.hwdb


