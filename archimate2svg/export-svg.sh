#!/bin/bash

archi_settings="/root/.archi4"
source_file="/external/"$1
destination_file="/external/"$2

rm $destination_file
rm -rf $archi_settings
mkdir -p $archi_settings/.metadata/.plugins/org.eclipse.core.runtime/.settings/
printf "eclipse.preferences.version=1\nshowIntro=false" | tee $archi_settings/.metadata/.plugins/org.eclipse.core.runtime/.settings/org.eclipse.ui.prefs
printf '<?xml version="1.0" encoding="UTF-8"?><models><model file="'$source_file'" /></models>' | tee $archi_settings/models.xml
printf "ExportImageLastFile=$destination_file\nExportImageLastProvider=com.archimatetool.export.svg.imageExporter\neclipse.preferences.version=1" | tee $archi_settings/.metadata/.plugins/org.eclipse.core.runtime/.settings/com.archimatetool.editor.prefs

Xvfb $DISPLAY -screen 0 1366x768x16 &
sleep 2
/Archi/Archi &
sleep 8

xdotool search --name "Archi" | tail --line 1 | while read each_window;
do
    xdotool mousemove --window $each_window 50 150 click 1
    xdotool mousedown 1;xdotool mouseup 1
    xdotool key --window $each_window Right End Right End Return
    xdotool key --window $each_window Return alt+f e Down Down Return
    xdotool key --window $each_window Return
    sleep 2
    xdotool key --window $each_window alt+f x 
done
    
