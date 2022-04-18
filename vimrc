" Not use VI keyboard setting
set nocompatible
" Set line number
set number

syntax on
filetype on
filetype plugin on
filetype indent on

" Indentation
set tabstop=4
set softtabstop=4
set shiftwidth=4
set expandtab  " Replace Tabs with Spaces
set autoindent " Add indent when starting a new line
set smartindent

" Jump to the last position when reopening a file
if has("autocmd")
    au BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g'\"" | endif
endif

" ----------------------------------------
"
"       Indentation based on filetype
"
" ----------------------------------------

" Tab characters are required in makefile
autocmd FileType make set noexpandtab tabstop=8 shiftwidth=8 softtabstop=0


" Display Tabs and Spaces
set listchars=tab:>-,trail:-
set list

" Search and match
set hlsearch  " Highlight search
set incsearch " Real time display searching result
set showmatch " Show the matching bracket and brace
" set ignorecase
" set smartcase

set nobackup
set backspace=indent,eol,start

set tabpagemax=20

set background=dark
set t_Co=256
set t_ut=

colorscheme codedark
hi SpecialKey ctermfg=240

" colorscheme  molokai
" let g:rehash256 = 1
" let g:molokai_original = 1

" Install plugin management: vim-plug
let data_dir = has('nvim') ? stdpath('data') . '/site' : '~/.vim'
if empty(glob(data_dir . '/autoload/plug.vim'))
  silent execute '!curl -fLo '.data_dir.'/autoload/plug.vim --create-dirs  https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
  autocmd VimEnter * PlugInstall --sync | source $MYVIMRC
endif

" Run PlugInstall if there are missing plugins
autocmd VimEnter * if len(filter(values(g:plugs), '!isdirectory(v:val.dir)'))
  \| PlugInstall --sync | source $MYVIMRC
\| endif

" Open files with the cursor on when the file was closed
if has("autocmd")
  au BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g'\"" | endif
endif

" ----------------------------------------
"
"            Install/Call Plugins
"
" ----------------------------------------

call plug#begin('~/.vim/plugged')
Plug 'scrooloose/nerdtree'
Plug 'ervandew/supertab'
Plug 'tpope/vim-surround'
Plug 'tpope/vim-fugitive'
Plug 'ctrlpvim/ctrlp.vim'
Plug 'majutsushi/tagbar'
Plug 'godlygeek/tabular'
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'
"Plug 'mhinz/vim-startify' " Quick access to recent files
Plug 'junegunn/fzf.vim'
Plug 'preservim/nerdcommenter'
Plug 'nachumk/systemverilog.vim'
Plug 'bfrg/vim-cpp-modern'

if executable('man')
    Plug 'murukeshm/vim-manpager'
endif

if has("lua") && v:version > 703 && v:version < 802
    Plug 'Shougo/neocomplete.vim'
else
    if executable('cmake')
        Plug 'Valloric/YouCompleteMe'
    endif
endif
call plug#end()

" ----------------------------------------
"
"           NERDTree configuration
"
" ----------------------------------------

" Exit Vim if NERDTree is the only window left.
autocmd BufEnter * if tabpagenr('$') == 1 && winnr('$') == 1 && exists('b:NERDTree') && b:NERDTree.isTabTree() |
    \ quit | endif

" ----------------------------------------
"
"           supertab configuration
"
" ----------------------------------------
let g:SuperTabRetainCompletionType = 2
let g:SuperTabDefaultCompletionType = "<C-X><C-O>"

" ----------------------------------------
"
"           tagbar configuration
"
" ----------------------------------------
let g:tagbar_ctags_bin = 'ctags'
" let g:tagbar_left = 1                "tagbar displayed on left side. Right by default
let g:tagbar_width = 30              "Width: 30 columns. Default:40
let g:tagbar_autofocus = 1           "Put the cursor in the tagbar window when it's opened
let g:tagbar_sort = 0                "No sort for tags. Sort by default

" ----------------------------------------
"
"       The-Nerd-Commenter configuration
"
" ----------------------------------------
" Create default mappings
let g:NERDCreateDefaultMappings = 1

" Add spaces after comment delimiters by default
let g:NERDSpaceDelims = 1

" Use compact syntax for prettified multi-line comments
let g:NERDCompactSexyComs = 1

" Align line-wise comment delimiters flush left instead of following code indentation
let g:NERDDefaultAlign = 'left'

" Set a language to use its alternate delimiters by default
let g:NERDAltDelims_cpp = 1

" Add your own custom formats or override the defaults
" let g:NERDCustomDelimiters = { 'c': { 'left': '/**','right': '*/' } }

" Allow commenting and inverting empty lines (useful when commenting a region)
let g:NERDCommentEmptyLines = 1

" Enable trimming of trailing whitespace when uncommenting
let g:NERDTrimTrailingWhitespace = 1

" Enable NERDCommenterToggle to check all selected lines is commented or not 
let g:NERDToggleCheckAllLines = 1

" ----------------------------------------
"
"         vim-airline configuration
"
" ----------------------------------------
" Uncomment it when encountering something like '>4,2'
" let &t_TI = ""
" let &t_TE = ""

let g:airline#extensions#tabline#enabled = 1
let g:airline#extensions#tabline#left_sep = ' '
let g:airline#extensions#tabline#left_alt_sep = '|'
let g:airline#extensions#tabline#buffer_nr_show = 1

let g:airline_theme='ayu_dark'
let laststatus = 2
" let g:airline_powerline_fonts = 1

" ----------------------------------------
"
"        YouCompleteMe configuration
"
" ----------------------------------------

let g:ycm_filetype_blacklist = {
      \ 'tagbar' : 1,
      \ 'qf' : 1,
      \ 'notes' : 1,
      \ 'markdown' : 1,
      \ 'unite' : 1,
      \ 'text' : 1,
      \ 'vimwiki' : 1,
      \ 'pandoc' : 1,
      \ 'infolog' : 1,
      \ 'mail' : 1
      \}
" Disable preview window after accepting the completion
set completeopt-=preview
" Mock IDE
set completeopt=longest,menu
" Use tag files generated by ctags
let g:ycm_collect_identifiers_from_tag_files = 1
" Enable completion in comments
let g:ycm_complete_in_comments=1
" Enable completion in strings
let g:ycm_complete_in_strings=1
" Enable syntax completion
let g:ycm_seed_identifiers_with_syntax=1
" Auto-close preview window after select a completion string
let g:ycm_autoclose_preview_window_after_completion=1
" Close preview window after leaving insert mode
let g:ycm_autoclose_preview_window_after_insertion=1
" Trigger semantic completion after inserting 3 characters
let g:ycm_semantic_triggers =  {
            \ 'c,cpp,python,java,go,erlang,perl': ['re!\w{3}'],
            \ 'cs,lua,javascript': ['re!\w{3}'],
            \ }


" -----------------------------------------
"
"    neocomplete official configuration
"
" -----------------------------------------
if exists('g:load_neocomplete')

"Note: This option must be set in .vimrc(_vimrc).  NOT IN .gvimrc(_gvimrc)!
" Disable AutoComplPop.
let g:acp_enableAtStartup = 0
" Use neocomplete.
let g:neocomplete#enable_at_startup = 1
" Use smartcase.
let g:neocomplete#enable_smart_case = 1
" Set minimum syntax keyword length.
let g:neocomplete#sources#syntax#min_keyword_length = 3

" Define dictionary.
let g:neocomplete#sources#dictionary#dictionaries = {
    \ 'default' : '',
    \ 'vimshell' : $HOME.'/.vimshell_hist',
    \ 'scheme' : $HOME.'/.gosh_completions'
        \ }

" Define keyword.
if !exists('g:neocomplete#keyword_patterns')
    let g:neocomplete#keyword_patterns = {}
endif
let g:neocomplete#keyword_patterns['default'] = '\h\w*'

" Plugin key-mappings.
inoremap <expr><C-g>     neocomplete#undo_completion()
inoremap <expr><C-l>     neocomplete#complete_common_string()

" Recommended key-mappings.
" <CR>: close popup and save indent.
inoremap <silent> <CR> <C-r>=<SID>my_cr_function()<CR>
function! s:my_cr_function()
  return (pumvisible() ? "\<C-y>" : "" ) . "\<CR>"
  " For no inserting <CR> key.
  "return pumvisible() ? "\<C-y>" : "\<CR>"
endfunction
" <TAB>: completion.
inoremap <expr><TAB>  pumvisible() ? "\<C-n>" : "\<TAB>"
" <C-h>, <BS>: close popup and delete backword char.
inoremap <expr><C-h> neocomplete#smart_close_popup()."\<C-h>"
inoremap <expr><BS> neocomplete#smart_close_popup()."\<C-h>"
" Close popup by <Space>.
"inoremap <expr><Space> pumvisible() ? "\<C-y>" : "\<Space>"

" AutoComplPop like behavior.
"let g:neocomplete#enable_auto_select = 1

" Shell like behavior(not recommended).
"set completeopt+=longest
"let g:neocomplete#enable_auto_select = 1
"let g:neocomplete#disable_auto_complete = 1
"inoremap <expr><TAB>  pumvisible() ? "\<Down>" : "\<C-x>\<C-u>"

" Enable omni completion.
autocmd FileType css setlocal omnifunc=csscomplete#CompleteCSS
autocmd FileType html,markdown setlocal omnifunc=htmlcomplete#CompleteTags
autocmd FileType javascript setlocal omnifunc=javascriptcomplete#CompleteJS
autocmd FileType python setlocal omnifunc=pythoncomplete#Complete
autocmd FileType xml setlocal omnifunc=xmlcomplete#CompleteTags

" Enable heavy omni completion.
if !exists('g:neocomplete#sources#omni#input_patterns')
  let g:neocomplete#sources#omni#input_patterns = {}
endif
"let g:neocomplete#sources#omni#input_patterns.php = '[^. \t]->\h\w*\|\h\w*::'
"let g:neocomplete#sources#omni#input_patterns.c = '[^.[:digit:] *\t]\%(\.\|->\)'
"let g:neocomplete#sources#omni#input_patterns.cpp = '[^.[:digit:] *\t]\%(\.\|->\)\|\h\w*::'

" For perlomni.vim setting.
" https://github.com/c9s/perlomni.vim
let g:neocomplete#sources#omni#input_patterns.perl = '\h\w*->\h\w*\|\h\w*::'

endif

" -----------------------------------------
"
"           Shortcuts Configuration
"
" ----------------------------------------

nnoremap <F2>  :NERDTreeToggle<CR>
nmap     <F8>  :TagbarToggle<CR>

nnoremap <C-F7> :resize +5<CR>
nnoremap <C-F6> :resize -5<CR>
nnoremap <F7>   :vertical res +5<CR>
nnoremap <F6>   :vertical res -5<CR>

nnoremap <F5>   :buffers<CR>:buffer<Space>
nnoremap <F4>   :buffers<CR>:bdelete<Space>

" Tab switch
nnoremap <C-n> gt
nnoremap <C-m> gT

" Window switch
nmap <C-j> <C-W>j
nmap <C-k> <C-W>k
nmap <C-h> <C-W>h
nmap <C-l> <C-W>l

inoremap <C-j> <Down>
inoremap <C-k> <Up>
inoremap <C-h> <Left>
inoremap <C-l> <Right>

" Use C-y to make copy under Visual Mode
vnoremap <C-y> "+y
" Use C-p to paste under Normal Mode
nnoremap <C-p> "*p

" -----------------------------------------
"
"         Filetype Auto Recongnition
"
" ----------------------------------------
autocmd BufNewFile,BufRead *.sv set filetype=verilog
" For NVIDIA
autocmd BufNewFile,BufRead *.vx,*.vcp set filetype=verilog


" -----------------------------------------
"
"              Common Function
"
" ----------------------------------------

" Change indent
function! s:Reindent(new_indent)
    let &l:tabstop = a:new_indent
    let &l:shiftwidth = a:new_indent
    let &l:softtabstop = a:new_indent
endfunction

command -nargs=1 Reindent call s:Reindent(<f-args>)

