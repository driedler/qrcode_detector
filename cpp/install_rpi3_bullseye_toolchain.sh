#!/bin/sh

set -e

CMAKE_URL=https://github.com/Kitware/CMake/releases/download/v3.25.1/cmake-3.25.1-linux-x86_64.sh
RPI_ROOTFS_URL=https://www.dropbox.com/s/q5gwd91j9gcbclm/rpi_bullseye_rootfs.7z?dl=1


sudo apt-get update  
sudo apt-get upgrade -y
sudo apt-get remove -y cmake
sudo apt-get install -y ninja-build p7zip-full build-essential pkg-config libjpeg-dev libtiff5-dev libpng-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libatlas-base-dev gfortran  python3-dev
sudo apt-get install -y ffmpeg
sudo apt-get install -y crossbuild-essential-armhf gawk pkg-config git pkg-config-arm-linux-gnueabihf sshfs


echo "Downloading $CMAKE_URL"
wget -O /tmp/cmake_install.sh $CMAKE_URL

echo "Updating CMake"
sudo chmod +x /tmp/cmake_install.sh
sudo /tmp/cmake_install.sh --skip-license --prefix=/usr

echo "Downloading $RPI_ROOTFS_URL"
wget -O /tmp/rpi_bullseye_rootfs.7z $RPI_ROOTFS_URL

echo "Extracting RPI root FS to $HOME/rpi/rootfs"
mkdir -p $HOME/rpi/rootfs
7z x /tmp/rpi_bullseye_rootfs.7z -y -o$HOME/rpi/rootfs