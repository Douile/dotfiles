#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

# Load bash completions
source /usr/share/bash-completion/bash_completion

alias ls='ls --color=auto'

# Save overwrite
alias cp='cp -i'
alias mv='mv -i'
alias rm='rm -i'

# PS1='[\u@\h \W]\$ '
PS1="\[\033[38;5;14m\]\u\[$(tput sgr0)\]@\[$(tput sgr0)\]\[\033[38;5;9m\]\h\[$(tput sgr0)\]:\[$(tput sgr0)\]\[\033[38;5;46m\]\W\[$(tput sgr0)\]\\$ \[$(tput sgr0)\]"export PS1="\[\033[38;5;14m\]\u\[$(tput sgr0)\]@\[$(tput sgr0)\]\[\033[38;5;9m\]\h\[$(tput sgr0)\]:\[$(tput sgr0)\]\[\033[38;5;46m\]\W\[$(tput sgr0)\]\\$ \[$(tput sgr0)\]"

# View the qtile log with vim
alias qtile-log="tail ~/.local/share/qtile/qtile.log"
# Restart qtile
alias qtile-restart="qtile-cmd -o cmd -f restart"
# Use the git bare config
alias config="git --work-tree=$HOME --git-dir=$HOME/.dotfiles"
# Tell ssh we're xterm-color
alias ssh="TERM=\"xterm-color\" ssh"

alias cycle_vpn="nmcli connection down client-win10 && nmcli connection up client-win10"

# Load bash-scripts from https://github.com/Douile/bash-scripts
source ~/Software/bash-scripts/source.sh
