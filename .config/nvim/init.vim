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
NeoBundle 'Shougo/deoplete.nvim', { 'do': ':UpdateRemotePlugins' }
NeoBundle 'Shougo/neosnippet.vim'
NeoBundle 'Shougo/neosnippet-snippets'
NeoBundle 'tpope/vim-fugitive'
NeoBundle 'ctrlpvim/ctrlp.vim'
NeoBundle 'Shougo/vimshell'

" Own bundles
NeoBundle 'cespare/vim-toml'
"NeoBundle 'pucka906/vdrpc'
NeoBundle 'rust-lang/rust.vim'
NeoBundle 'vim-airline/vim-airline'
NeoBundle 'joshdick/onedark.vim'
NeoBundle 'tomlion/vim-solidity'
NeoBundle 'lervag/vimtex'
NeoBundle 'skywind3000/asyncrun.vim'

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
set colorcolumn=80

" Don't expand tabs in make files
autocmd FileType make setlocal noexpandtab

" Auto-reloads
autocmd BufWritePost ~/.i3/config silent exec "!(i3-msg restart) > /dev/null"
autocmd BufWritePost ~/.config/i3status/config silent exec "!(i3-msg restart) > /dev/null"
autocmd BufWritePost ~/.config/i3status/i3status.sh silent exec "!(i3-msg restart) > /dev/null"
autocmd BufWritePost ~/.config/qtile/config.py silent exec "!(qtile cmd-obj -o cmd -f restart 2>/dev/null) > /dev/null"
" autocmd BufWritePost ~/.profile silent exec "!(source ~/.profile)"
" autocmd BufWritePost ~/.bashrc silent exec "!(source ~/.bashrc)"

" Code beautify
autocmd BufWritePost *.java
                    \ silent exec "!astyle --indent=spaces=2 -c -xb -j -xf -xh -U -D -xg -p -H -f -C -S --mode=java --style=java -z2 %" |
                    \ e
autocmd BufWritePost *.rs
                    \ silent exec "!cargo fmt" |
                    \ e
autocmd BufWritePost *.js
                    \ silent exec "!js-beautify -s 2 -f %" |
                    \ e
autocmd BufWritePost *.md
                    \ exec "AsyncRun -pos=bottom ./build.sh"

" Switch tab binds
nnoremap <C-j> :tabprevious<CR>
nnoremap <C-k> :tabnext<CR>

colorscheme onedark
syntax on

" Neosnippet options
" Enable snipMate compatibility feature.
"let g:neosnippet#enable_snipmate_compatibility = 1
"let g:deoplete#enable_at_startup = 1
"inoremap <expr><tab> pumvisible() ? deoplete#manual_complete() : "\<tab>"

" VDRPC options
let g:vdrpc_filesize = 1
let g:vdrpc_autostart = 1

" rust options
let g:rustfmt_autosave = 1

" Ariline options
let g:airline#extensions#tabline#enabled = 1
let g:airline_theme='onedark'
"let g:airline_powerline_fonts = 1

let g:asyncrun_status=''
let g:airline_section_error=airline#section#create_right(['%{g:asyncrun_status}'])
