#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='ls --color=auto'

# Save overwrite
alias cp='cp -i'
alias mv='mv -i'
alias rm='rm -i'

PS1='[\u@\h \W]\$ '

# View the qtile log with vim
alias qtile-log="tail ~/.local/share/qtile/qtile.log"
# Restart qtile
alias qtile-restart="qtile-cmd -o cmd -f restart"
# Use the git bare config
alias config="git --work-tree=$HOME --git-dir=$HOME/.dotfiles"

# Load bash-scripts from https://github.com/Douile/bash-scripts
source ~/Software/bash-scripts/source.sh
