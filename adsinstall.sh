mkdir AdsBlocker
cd AdsBlocker
apt update && apt upgrade -y
apt install unzip
wget https://github.com/TheMrMobin/AdsBlocker/archive/refs/heads/main.zip
clear
unzip main.zip
cd AdsBlocker-main
python3 adsblocker.py