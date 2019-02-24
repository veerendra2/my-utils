#!/bin/bash
# Author: Veerendra Kakumanu
# Description: Create br0 bridge, configures NAT rules on it. Usefull when VM are connected to br0 bridge


EXTERNAL_IFACE="wlan0"
BR_ADDR="10.200.1.1/24"
SUBNET="10.200.1.0/24"
BR_NAME="br0"

# Creat br0 bridge
echo "[*] Creating $BR_NAME bridge"
sudo ip link add name $BR_NAME type bridge 2>/dev/null
sudo ip link set dev $BR_NAME up 2>/dev/null
sudo ip addr add $BR_ADDR dev $BR_NAME 2>/dev/null

# iptables NAT configuration
echo "[*] Adding NAT iptables rules for $BR_NAME"
sudo iptables -t nat -A POSTROUTING -o $EXTERNAL_IFACE -j MASQUERADE
sudo iptables -A FORWARD -i $EXTERNAL_IFACE -o $BR_NAME -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i $BR_NAME -o $EXTERNAL_IFACE -j ACCEPT

# Disable bridge-nf parameters(Can ssh into install instances)
# https://unix.stackexchange.com/questions/490893/not-able-to-ssh-from-vm-to-vm-via-linux-bridge
echo "[*] Disabling bridge-nf parameters"
sudo sysctl -w net.bridge.bridge-nf-call-arptables=0
sudo sysctl -w net.bridge.bridge-nf-call-ip6tables=0
sudo sysctl -w net.bridge.bridge-nf-call-iptables=0

# Creates docker network with bridge
# https://docs.docker.com/config/containers/container-networking/
echo "[*] Creating docker network with bridge $BR_NAME"
sudo docker network create --driver=bridge --ip-range=$SUBNET --subnet=$SUBNET -o "com.docker.network.bridge.name=br0" $BR_NAME
