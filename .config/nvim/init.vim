"NeoBundle Scripts-----------------------------
if has('vim_starting')
  " Required:
  set runtimepath+=~/.config/nvim/bundle/neobundle.vim/
endif

" Required:
call neobundle#begin(expand('~/.config/nvim/bundle'))

" Let NeoBundle manage NeoBundle
" Required:
NeoBundleFetch 'Shougo/neobundle.vim'

" Add or remove your Bundles here:
" Default bundles"
NeoBundle 'Shougo/neosnippet.vim'
NeoBundle 'Shougo/neosnippet-snippets'
NeoBundle 'tpope/vim-fugitive'
NeoBundle 'ctrlpvim/ctrlp.vim'
NeoBundle 'flazz/vim-colorschemes'
NeoBundle 'Shougo/vimshell'

" Own bundles
NeoBundle 'cespare/vim-toml'
NeoBundle 'pucka906/vdrpc'

" Required:
call neobundle#end()

" Required:
filetype plugin indent on

" If there are uninstalled bundles found on startup,
" this will conveniently prompt you to install them.
NeoBundleCheck
"End NeoBundle Scripts-------------------------

" Custom config
set number
set ts=2 sw=2
set expandtab

" Don't expand tabs in make files
autocmd FileType make setlocal noexpandtab

" Auto-reloads
autocmd BufWritePost ~/.i3/config silent exec "!(i3-msg restart) > /dev/null"
autocmd BufWritePost ~/.config/i3status/config silent exec "!(i3-msg restart) > /dev/null"
autocmd BufWritePost ~/.config/i3status/i3status.sh silent exec "!(i3-msg restart) > /dev/null"
autocmd BufWritePost ~/.config/qtile/config.py silent exec "!(qtile-cmd -o cmd -f restart 2>/dev/null) > /dev/null"
autocmd BufWritePost ~/.profile silent exec "!(source ~/.profile)"

" Switch tab binds
nnoremap <C-j> :tabprevious<CR>
nnoremap <C-k> :tabnext<CR>

syntax on

" VDRPC options
let g:vdrpc_filesize = 1
let g:vdrpc_autostart = 1

