#!/bin/bash

sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target

# only on first boot
if ! command -v nvcc &> /dev/null
then

    sudo bash -c "echo blacklist nouveau > /etc/modprobe.d/blacklist-nvidia-nouveau.conf"
    sudo bash -c "echo options nouveau modeset=0 >> /etc/modprobe.d/blacklist-nvidia-nouveau.conf"
	
    sudo apt update
    sudo apt -y install python3-pip python3-dev
    sudo pip3 install --upgrade pip

    sudo wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-keyring_1.0-1_all.deb -O /tmp/cuda-keyring_1.0-1_all.deb
    sudo dpkg -i /tmp/cuda-keyring_1.0-1_all.deb
    sudo apt update
    sudo apt-get clean
    sudo apt -y install linux-headers-$(uname -r)
    sudo apt -y install cuda-11-8
    sudo apt-get clean
    sudo apt -y install nvidia-gds
    sudo apt-get clean
    sudo apt -y install libcudnn8
    sudo apt-get clean

    echo 'PATH="/usr/local/cuda-11.8/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin"' | sudo tee /etc/environment
    
    sudo chown $USER /data
    mkdir -p /data/tmp
    TMPDIR=/data/tmp python3 -m pip install --cache-dir=/data/tmp --target=/data Cython==0.29.32
    TMPDIR=/data/tmp python3 -m pip install --cache-dir=/data/tmp --target=/data -r /local/repository/requirements_cloudlab_dl.txt --extra-index-url https://download.pytorch.org/whl/cu113 -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html
    TMPDIR=/data/tmp python3 -m pip install --cache-dir=/data/tmp --target=/data jupyter-core jupyter-client jupyter_http_over_ws traitlets -U --force-reinstall

fi

