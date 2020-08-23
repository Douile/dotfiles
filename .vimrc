" Numbering
set number

" Tabs
set expandtab
set tabstop=2 shiftwidth=2
retab

" Don't use spaces in make files
autocmd FileType make setlocal noexpandtab

" Auto-remloads
autocmd BufWritePost ~/.i3/config silent exec "!(i3-msg restart) > /dev/null"
autocmd BufWritePost ~/.config/i3status/config silent exec "!(i3-msg restart) > /dev/null"
autocmd BufWritePost ~/.config/i3status/i3status.sh silent exec "!(i3-msg restart) > /dev/null"

" Change window binds
nnoremap <C-J> <C-W><C-J>
nnoremap <C-K> <C-W><C-K>
nnoremap <C-L> <C-W><C-L>
nnoremap <C-H> <C-W><C-H>

" Other
syntax on
