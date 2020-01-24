#!/bin/bash
# Author: Veerendra Kakumanu
# Description: Arrays in shell

# 1 Dimentional Arrays Decloration
packages=(
"systemtap" "iotop"
"blktrace" "sysdig"
"sysstat" "linux-tools-common"
)

# 2 Dimentional Arrays Decloration
declare -A ppa_pkgs=(
  ['atom']="ppa:webupd8team/atom"
  ['wireshark']="ppa:wireshark-dev/stable"
  ['anoise']="ppa:costales/anoise"
)

echo "All items  --> ${packages[*]}"
echo "ONLY items --> ${ppa_pkgs[*]}"
echo "Keys and Values --> ${ppa_pkgs[@]}"
echo "Only key --> ${!ppa_pkgs[@]}"

# Iterate key,value
for i in "${!ppa_pkgs[@]}"
do
  echo "key  : $i"
  echo "value: ${ppa_pkgs[$i]}"
done

