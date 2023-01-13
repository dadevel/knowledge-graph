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

References:

- [THC's favorite tips, tricks & hacks](https://github.com/hackerschoice/thc-tips-tricks-hacks-cheat-sheet/)
