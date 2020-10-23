#!/bin/sh

FILE="$HOME/Pictures/sc-$(date +%Y-%m-%d-%H-%M-%S).png";
maim -s -u | tee "$FILE" | xclip -selection clipboard -t image/png && {
  action=$(dunstify -a "maim" --action="show,Show in file explorer" -i "$FILE" "Screeshotted" "File saved as $FILE")
  if test $action = 2; then
    setsid pcmanfm $(dirname "$FILE")
  fi
}
