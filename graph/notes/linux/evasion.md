---
title: Linux Evasion
---

[[notes/mitre-attack/defense-evasion]] tricks for [[notes/linux/index]].

Disable `bash` history.

~~~ bash
unset HISTFILE
~~~

Hide suspicious process names with `bash`.

~~~ bash
exec -a syslogd nmap -A 10.0.2.1/24
~~~

Hide processes without `bash`.

~~~ bash
cp `which nmap` ./syslogd
PATH=".:$PATH" syslogd -A 10.0.2.1/24
~~~

Log in over SSH but hide from `/var/log/utmp` and `who`, won't load `.bash_profile`.

~~~ bash
ssh -T user@192.0.2.1 'bash -i'
~~~

Clear log file without restarting `syslogd`.

~~~ bash
cat /dev/null > /var/log/auth.log
~~~

Execute binary without `x` permission.

~~~ bash
/lib/ld-linux*.so* /dev/shm/pwn
~~~

Untested tools:

- [fuse-loader](https://github.com/EvanMcBroom/fuse-loader), loads dynamic library from memory trough fuse mount
- Linux in-memory execution techniques from [Strategies to bypass Read-Only, No-Exec, and Distroless Environments - DEF CON 31](http://web.archive.org/web/20230814075243/https://media.defcon.org/DEF%20CON%2031/DEF%20CON%2031%20presentations/Carlos%20Polop%20Yago%20Gutierrez%20-%20Exploring%20Linux%20Memory%20Manipulation%20for%20Stealth%20and%20Evasion%20Strategies%20to%20bypass%20Read-Only%20No-Exec%20and%20Distroless%20Environments.pdf)
    - [DistrolessRCE](https://github.com/carlospolop/DistrolessRCE)
    - [memdlopen](https://github.com/arget13/memdlopen)
    - [memexec](https://github.com/arget13/memexec)
    - [ddexec](https://github.com/arget13/DDexec)

References:

- [THC's favorite tips, tricks & hacks](https://github.com/hackerschoice/thc-tips-tricks-hacks-cheat-sheet/)
