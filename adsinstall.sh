#!/bin/bash


if ! dpkg -l | grep -qw unzip; then
    echo "Installing unzip..."
    sudo apt update
    sudo apt install -y unzip
fi


if ! python3 -c "import tqdm" &> /dev/null; then
    echo "Installing tqdm..."
    pip install tqdm
fi


if [ ! -d "AdsBlocker" ]; then
    echo "Creating AdsBlocker directory..."
    mkdir AdsBlocker
fi


cd AdsBlocker


if [ ! -f "main.zip" ]; then
    echo "Downloading main.zip..."
    wget https://github.com/TheMrMobin/AdsBlocker/archive/refs/heads/main.zip
else
    echo "main.zip already exists, skipping download."
fi


if [ ! -d "AdsBlocker-main" ]; then
    echo "Unzipping main.zip..."
    unzip main.zip
else
    echo "AdsBlocker-main already exists, skipping unzip."
fi


cd AdsBlocker-main


echo "Running adsblocker.py..."
python3 adsblocker.py
