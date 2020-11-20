#!/bin/sh

FNAME="$(date +%F-%T)-scrot.png"
maim -s | tee "$HOME/Pictures/$FNAME" | xclip -selection clipboard -t image/png && notify-send "Screen shotted as $FNAME"
