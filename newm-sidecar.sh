#!/bin/bash
ADDR=$(ip -o -4 addr list wlan0 | awk '{print $4}' | cut -d/ -f1)
SCRIPTDIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

URL=$(python3 $SCRIPTDIR/newm_sidecar.py)
URL=${URL/localhost/$ADDR}
qrencode -m 2 -t utf8 <<< "$URL"

if  [ "$1" != "-y" ]; then
    read -p "Continue? [Y/n]" confirm && [[ $confirm == [yY] || -z $confirm ]] || exit 1
fi

newm-cmd open-virtual-output virt-1
trap 'newm-cmd close-virtual-output virt-1' EXIT

sleep .2
wayvnc --output=virt-1 --max-fps=30 localhost 5900
