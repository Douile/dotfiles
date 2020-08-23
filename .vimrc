set number
set tabstop=2
retab

autocmd BufWritePost ~/.i3/config silent exec "!(i3-msg restart) > /dev/null"
autocmd BufWritePost ~/.config/i3status/config silent exec "!(i3-msg restart) > /dev/null"
autocmd BufWritePost ~/.config/i3status/i3status.sh silent exec "!(i3-msg restart) > /dev/null"

syntax on
