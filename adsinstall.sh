apt update && apt upgrade -y
apt install unzip
mkdir AdsBlocker
cd AdsBlocker
wget https://github.com/TheMrMobin/AdsBlocker/archive/refs/heads/main.zip
clear
unzip main.zip
cd AdsBlocker-main
python3 adsblocker.py
