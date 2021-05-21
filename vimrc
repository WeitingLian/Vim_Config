" Not use VI keyboard setting
set nocompatible
" Set line number
set number

syntax on
filetype on

" Indentation
set tabstop=4
set softtabstop=4
set shiftwidth=4
set expandtab  " Replace Tabs with Spaces
set autoindent " Add indent when starting a new line
set smartindent

" Display Tabs and Spaces
set listchars=tab:-,trail:-
set list

" Search and match
set hlsearch  " Highlight search
set incsearch " Real time display searching result
set showmatch " Show the matching bracket and brace
" set ignorecase
" set smartcase

set nobackup


set guifont=Courier\ New\ 11


" colorscheme  molokai
" set t_Co=256
" set background=dark


call plug#begin('~/.vim/plugged')
Plug 'scrooloose/nerdtree'
Plug 'vim-airline/vim-airline'
call plug#end()
