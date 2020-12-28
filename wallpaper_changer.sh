#!/bin/bash
export DISPLAY=:0
export XAUTHORITY=/home/pi/.Xauthority
export XDG_RUNTIME_DIR=/run/user/1000
pcmanfm --set-wallpaper=$1 --wallpaper-mode=crop
