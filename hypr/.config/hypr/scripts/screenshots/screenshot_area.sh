#!/bin/bash
savePath=$(date +'screenshot_%Y-%m-%d-%H%M%S.png')
grim -g "$(slurp)" $HOME/Pictures/Screenshots/"$savePath"
notify-send "screenshot saved to $savePath" -t 1000
