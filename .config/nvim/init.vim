"NeoBundle Scripts-----------------------------
if has('vim_starting')
  " Required:
  set runtimepath+=/home/user/.config/nvim/bundle/neobundle.vim/
endif

" Required:
call neobundle#begin(expand('/home/user/.config/nvim/bundle'))

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

"Custom config
set number
set ts=2 sw=2
set expandtab

autocmd FileType make setlocal noexpandtab

nnoremap <C-j> :tabprevious<CR>
nnoremap <C-k> :tabnext<CR>

syntax on

" VDRPC options
let g:vdrpc_filesize = 1
let g:vdrpc_autostart = 1

