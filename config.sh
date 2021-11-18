#!usr/bin/sh

if [! -d "~/.vim"]; then
    mkdir ~/.vim
fi

if [! -f "~/.vim/vimrc"]; then
    rm ~/.vim/vimrc
fi

cp vimrc ~/.vim/

if [! -d "~/.vim/colors"]; then
    cp -r ./colors ~/.vim
fi

