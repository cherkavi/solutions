#!/bin/bash
###                   TODO 
###
# print all monitors 
# xrandr | grep " connected"
WIDTH=2000
HEIGHT=1200
OUTPUT_NAME=VIRTUAL1
EXISTING_SCREEN="DP-2.1"
if [ "$1" == "create" ]; then
  # 
  gtf $WIDTH $HEIGHT 60 | sed '3q;d' | sed 's/Modeline//g' | xargs xrandr --newmode
  
  #  cvt 1920 1080 60
  # xrandr --newmode "192010802"  201.50  2000 2136 2352 2704  1200 1201 1204 1242  -HSync +Vsync
  # xrandr --addmode DP-2 2000x1200_60.00
  # xrandr --output DP-2 --left-of $EXISTING_SCREEN --mode "2000x1200"  

  # sed: get third line, delete 'Modeline', get first word, remove first and last characters
  gtf $WIDTH $HEIGHT 60 | sed '3q;d' | sed 's/Modeline//g' | awk '{print $1;}' | sed 's/^.\(.*\).$/\1/' | xargs xrandr --addmode $OUTPUT_NAME
  gtf $WIDTH $HEIGHT 60 | sed '3q;d' | sed 's/Modeline//g' | awk '{print $1;}' | sed 's/^.\(.*\).$/\1/' | xargs xrandr --output $OUTPUT_NAME --left-of $EXISTING_SCREEN --mode
elif [ "$1" == "on" ]; then
  # x11vnc -listen 192.168.42.149 -clip ${WIDTH}x${HEIGHT}+0+0
  # For use in Wi-Fi LAN.
  x11vnc -clip ${WIDTH}x${HEIGHT}+0+0 #**WARNING** Unencrypted stream. VNC accessible without password through port 5900 in all internet interfaces.
else
  echo "missing argument: [create | on | off]"
fi