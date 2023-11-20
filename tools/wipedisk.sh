#!/usr/bin/env bash
# Author : Veeredra K
# Description : Fills zeros in empty spaces
# Reference : https://superuser.com/questions/19326/how-to-wipe-free-disk-space-in-linux
# Similar Tools : zerofree, secure-delete, shred

smallfile=/zero.small.file
file=/zero.file

rand_smallfile=/random.small.file
rand_file=/random.file

fast()
{
    dd if=/dev/zero of="$smallfile" bs=1024 count=102400
    dd if=/dev/zero of="$file" bs=1024
    sync ; sleep 60 ; sync
    rm zero.small.file
    rm zero.file
    if [ "$1" == "shutdown" ]; then
        sudo init 0
    elif [ "$1" == "reboot" ]; then
        sudo init 1
    fi

}

med()
{
    dd if=/dev/urandom of="$rand_smallfile" bs=1024 count=102400
    dd if=/dev/urandom of="$rand_file" bs=1024
    sync ; sleep 60 ; sync
    rm random.small.file
    rm random.file
    if [ "$1" == "shutdown" ]; then
        sudo init 0
    elif [ "$1" == "reboot" ]; then
        sudo init 1
    fi
}

slow()
{
    dd if=/dev/zero of="$smallfile" bs=1024 count=102400
    sync ; sleep 60 ; sync
    shred -z "$smallfile"
    dd if=/dev/zero of="$file" bs=1024
    sync ; sleep 60 ; sync
    rm "$smallfile"
    shred -z "$file"
    sync ; sleep 60 ; sync
    rm "$file"
    if [ "$1" == "shutdown" ]; then
        echo "shutdown"
    elif [ "$1" == "reboot" ]; then
        echo "reboot"
    fi
}

case "$1" in
    fast)
      fast $2
    ;;
    med)
      med $2
    ;;
    slow)
      slow $2
    ;;
esac
