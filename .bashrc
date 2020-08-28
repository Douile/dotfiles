#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='ls --color=auto'
alias cp='cp -i'

PS1='[\u@\h \W]\$ '

# View the qtile log with vim
alias qtile_log="vim ~/.local/share/qtile/qtile.log"
# Use the git bare config
alias config="git --work-tree=$HOME --git-dir=$HOME/.dotfiles"

# Load bash-scripts from https://github.com/Douile/bash-scripts
source ~/Software/bash-scripts/source.sh
