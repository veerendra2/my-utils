#!/bin/bash
echo "Installing TP-Link Wireless Nano USB Adapter(TL-WN725N) Drivers.[Internet Required!]"
sleep 3
apt-get update
apt-get install linux-headers-$(uname -r) build-essential git -y
git clone https://github.com/lwfinger/rtl8188eu.git
cd rtl8188eu
make clean
make all
make install
cp rtl8188eufw.bin /lib/firmware/rtlwifi/
insmod 8188eu.ko
echo "Please reboot your PC"
