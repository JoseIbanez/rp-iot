#!/bin/bash

sudo apt-get install -y lastpass-cli
mkdir -p ~/.config/lpass
mkdir -p ~/.local/share/lpass


echo "Note: first, lpass login [username]"
lpass status


mkdir -p ~/.secrets

#twitter auth (vlan200)
lpass show --notes "Veclas/twitter/vlan200" > ~/.secrets/twitter

