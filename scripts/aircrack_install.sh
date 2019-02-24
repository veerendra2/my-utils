#!/bin/bash
# Author: Veerendra Kakumanu
# Description: Installs Nvidia drivers, hashcat and aircrack-ng tool

sudo apt-update
echo "[+] Installing Nvidia Drivers"
sudo apt-get install nvidia-cuda-* -y
sudo ubuntu-drivers autoinstall
echo "[+] Installing Dependencies"
sudo apt-get install build-essential autoconf automake libtool pkg-config libnl-3-dev libnl-genl-3-dev libssl-dev ethtool shtool rfkill zlib1g-dev libpcap-dev libsqlite3-dev libpcre3-dev libhwloc-dev libcmocka-dev -y
download=`curl -s https://api.github.com/repos/aircrack-ng/aircrack-ng/releases/latest | grep tarball_url | cut -d '"' -f 4`
echo "[+] Downloading aircrack-ng latest version $version"
wget -q --show-progress $download -O aircrack_latest.tar
dir1=`tar -tf aircrack_latest.tar | head -1`
tar -xf aircrack_latest.tar
pushd $dir1
./autogen.sh
sudo make install -j`nproc`
popd
hashcat_download=`curl -s https://api.github.com/repos/hashcat/hashcat/releases/latest | grep browser_download_url | cut -d '"' -f 4`
echo "[+] Downloading hashcat binaries"
wget -q --show-progress $hashcat_download -O hashcat_latest.7z
dir2=`7z l hashcat_latest.7z | grep -i path | cut -d " " -f 3`
7z x hashcat_latest.7z
hashcatutils_url=`curl -s https://api.github.com/repos/hashcat/hashcat-utils/releases/latest | grep tarball_url | cut -d '"' -f 4`
echo "[+] Downloading hashcat utils"
wget -q --show-progress $hashcatutils_url -O hashcat_utils.tar
tar -xf hashcat_utils.tar -C $dir2
sudo mv $dir2 /opt/hashcat
echo "[*] Hashcat binaries directory moved to /opt"
echo "[+] Downloading rockyou.txt"
sudo wget -qO /opt/rockyou.txt --show-progress http://scrapmaker.com/data/wordlists/dictionaries/rockyou.txt
#https://phreaklets.blogspot.com/2013/06/cracking-wpa2-psk-passwords-with.html
