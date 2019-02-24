#!/bin/bash
echo "Installing TP-Link Wireless Nano USB Adapter(TL-WN725N) Drivers.[Internet Required!]"
sleep 3
sudo apt-get update
sudo apt-get install linux-headers-$(uname -r) build-essential git -y
git clone https://github.com/lwfinger/rtl8188eu.git
cd rtl8188eu
sudo make clean
sudo make all
sudo make install
sudo cp rtl8188eufw.bin /lib/firmware/rtlwifi/
sudo insmod 8188eu.ko
echo "Please reboot your PC"
