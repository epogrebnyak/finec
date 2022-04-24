#!/bin/bash 

git config pull.rebase true

# use poetry and install dependecies
pip install poetry
poetry install

# use just
# create ~/bin
mkdir -p ~/bin
# download and extract just to $HOME/.local/bin
# $HOME/.local/bin is on PATH
# PATH could not be changed to :$HOME/bin as intended earlier:
# 1) "postCreateCommand": "bash .devcontainer/post_create.sh",
# 2) "remoteEnv": {"PATH": "${containerEnv:PATH}:$HOME/bin"} 
# 3) echo 'export PATH="$PATH:$HOME/bin" ' >> $HOME/.bashrc 
# Neither of three above modifies PATH.
# Descibed at https://github.com/casey/just/issues/1164
curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to $HOME/.local/bin
# add `~/bin` to the paths that your shell searches for executables
# this line should be added to your shells initialization file,
# e.g. `~/.bashrc` or `~/.zshrc`
# export PATH="$PATH:$HOME/bin"
# echo 'export PATH="$PATH:$HOME/bin" ' >> $HOME/.bashrc
# just should now be executable
just --help
