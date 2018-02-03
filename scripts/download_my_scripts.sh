#!/usr/bin/env bash

sudo wget -qO /usr/local/bin/nettool https://raw.githubusercontent.com/veerendra2/useless-scripts/master/scripts/netTools.py7
sudo wget -qO /usr/local/bin/openvpn_auto https://raw.githubusercontent.com/veerendra2/useless-scripts/master/scripts/openvpn_auto.py
sudo wget -qO /usr/local/bin/httpserver https://github.com/veerendra2/useless-scripts/blob/master/scripts/httpserver.py
sudo wget -qO /usr/local/bin/pastebin https://raw.githubusercontent.com/veerendra2/useless-scripts/master/scripts/pastebin.py
sudo wget -qO /usr/local/bin/ssid_list https://raw.githubusercontent.com/veerendra2/useless-scripts/master/scripts/ssid_list.py
sudo chmod +x /usr/local/bin/ssid_list /usr/local/bin/pastebin /usr/local/bin/httpserver /usr/local/bin/openvpn_auto /usr/local/bin/nettool

sudo wget -qO /etc/init.d/changer https://raw.githubusercontent.com/veerendra2/useless-scripts/master/scripts/changer
sudo wget -qO /etc/init.d/encryptdns https://raw.githubusercontent.com/veerendra2/useless-scripts/master/scripts/encryptdns
sudo chmod +x /etc/init.d/encryptdns /etc/init.d/changer
sudo update-rc.d encryptdns defaults
sudo update-rc.d changer defaults
echo "Installed Scipts-> nettool, openvpn_auto, httpserver, pastebin, ssid_list"
