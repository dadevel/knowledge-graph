---
title: Linux Situational Awareness
---

Situational Awareness on [[notes/linux/index]].

# Basics

Environment variables.

~~~ bash
env || cat /proc/self/environ
~~~

Container checks.

~~~ bash
cat /.dockerenv
cat /etc/hosts
hostname || cat /etc/hostname
~~~

Files in the current directory.

~~~ bash
pwd
ls -la
~~~

OS and kernel version.

~~~ bash
cat /etc/issue
cat /usr/lib/os-release /etc/*release* | sort -Vu
uname -a || cat /proc/version
~~~

# Users

User and group info about the current user.

~~~ bash
id
~~~

User and group info about all local users.

~~~ bash
cat /etc/passwd
cat /etc/group
~~~

# Processes

Tree of running processes ([source](https://twitter.com/CraigHRowland/status/1701058386954170478)).

~~~ bash
ps -auxwwf | less -S
~~~

List of running processes.

~~~ bash
ps aux || cat /proc/sched_debug
~~~

Web server configs (Apache, Nginx, Lighttpd, Tomcat, ...).

~~~ bash
cat /etc/apache*/apache*.conf
ls -lA /etc/apache*/sites-enabled/*.conf
~~~

# Network

Network info.

~~~ bash
ip a || ifconfig
ip route || route || routel
~~~

Other reachable hosts.

~~~ bash
ip a
ip route
arp -a
cat /etc/hosts
~~~

Outgoing TCP connections.

~~~ bash
ss -anp || netstat -anp
~~~

Firewall rules (requires privileges).

~~~ bash
nft list ruleset || cat /etc/nftables.conf
iptables -L && ip6tables -L || cat /etc/iptables/*
~~~

# Filesystem

Disks and mountpoints.

~~~ bash
cat /etc/fstab
mount
ls -ld /dev/disk/by-id/*
lsblk
~~~
