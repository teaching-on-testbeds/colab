#!/bin/bash


if ! command -v nvcc &> /dev/null
then

    sudo apt update
    sudo apt -y install python3-pip python3-dev
    sudo pip3 install --upgrade pip

    sudo wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-keyring_1.0-1_all.deb -O /tmp/cuda-keyring_1.0-1_all.deb
    sudo dpkg -i /tmp/cuda-keyring_1.0-1_all.deb
    sudo apt update
    sudo apt-get clean
    sudo apt -y install linux-headers-$(uname -r)
    sudo apt -y install cuda
    sudo apt-get clean
    sudo apt -y install nvidia-gds
    sudo apt-get clean
    sudo apt -y install libcudnn8
    sudo apt-get clean

    echo 'PATH="/usr/local/cuda-11.8/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin"' | sudo tee /etc/environment
fi

