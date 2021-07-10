#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

# Load bash completions
source /usr/share/bash-completion/bash_completion

# Save overwrite
alias cp='cp -i'
alias mv='mv -i'
alias rm='rm -i'

# PS1='[\u@\h \W]\$ '
# PS1="\[\033[38;5;14m\]\u\[$(tput sgr0)\]@\[$(tput sgr0)\]\[\033[38;5;9m\]\h\[$(tput sgr0)\]:\[$(tput sgr0)\]\[\033[38;5;46m\]\W\[$(tput sgr0)\]\\$ \[$(tput sgr0)\]"export PS1="\[\033[38;5;14m\]\u\[$(tput sgr0)\]@\[$(tput sgr0)\]\[\033[38;5;9m\]\h\[$(tput sgr0)\]:\[$(tput sgr0)\]\[\033[38;5;46m\]\W\[$(tput sgr0)\]\\$ \[$(tput sgr0)\]"

HISTCONTROL=ignoreboth

# View the qtile log with vim
alias qtile-log="tail ~/.local/share/qtile/qtile.log"
# Restart qtile
alias qtile-restart="qtile-cmd -o cmd -f restart"
# Use the git bare config
alias config="git --work-tree=\"$HOME\" --git-dir=\"$HOME/.dotfiles\""
alias add="config add -u"
alias commit="config commit"
# Git aliases
alias gs="git status"
alias gd="git diff"
alias gdc="git diff --cached"
alias gap="git add -p"
alias gp="git push"
alias gb="git branch -lavv"
# Tell ssh we're xterm-color
alias ssh="TERM=\"xterm-256color\" ssh"
# Use exa instead of ls
alias ls='exa --group-directories-first -l'
alias sl="ls"
# Use nvim instead of vim
alias vim="nvim"

# Navigate fs
alias ..="cd .."
alias ...="cd ../.."

# Load starship prompt
eval "$(starship init bash)"

# Load bash-scripts from https://github.com/Douile/bash-scripts
source ~/Code/Github/bash-scripts/source.sh

# Get XMR price
# timeout 1 curl -s gbp.rate.sx/xmr
neofetch
