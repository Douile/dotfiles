#!/bin/sh

FILE="$HOME/Pictures/sc-$(date +%Y-%m-%d-%H-%M-%S).png";
maim -s -u $FILE
if test 0 -eq $?; then
  cat "$FILE" | xclip -selection clipboard -t image/png && {
    action=$(dunstify -a "maim" --action="show,Show in file explorer" -i "$FILE" "Screeshotted" "File saved as $FILE")
    echo "$action"
    if [ "$action" = "show" ]; then
      setsid pcmanfm $(dirname "$FILE")
    fi
  }
else
  dunstify -a "maim" -u critical "Screenshot" "Error taking screenshot"
fi
