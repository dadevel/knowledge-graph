---
title: SeDebugPrivilege
---

A [[notes/windows/privilege]] that allows to access the memory of any process and therefore escalation to local admin, e.g. by [[notes/windows/lsass-dump|dumping LSASS]].

Untested tools:

- [SeDebugPrivilegePoC](https://github.com/daem0nc0re/PrivFu/blob/main/PrivilegedOperations/SeDebugPrivilegePoC)

# GPO Bypass

The debug privilege can be disabled globally via a GPO, but this restriction can be bypassed.

Run `whoami /priv` as local admin and notice that `SeDebugPrivilege` is missing.

Export the current security policy to a file.

~~~ bat
secedit.exe /export /cfg secpolicy.inf /areas USER_RIGHTS
~~~

Edit `secpolicy.inf` to look like the following:

~~~
...
[Privilege Rights]
SeDebugPrivilege = *S-1-5-32-544
...
~~~

This allows the group of local administrators to use the debug privilege again.

Import the modified policy.

~~~ bat
echo J | secedit.exe /configure /db secedit.sdb /cfg secpolicy.inf /overwrite /areas USER_RIGHTS
~~~

In order for the changes to take effect you must log out and log in again.
The changes will stay in effect until the next GPO update cycle.

Alternatively you can abuse [[notes/windows/lsass-dump-builtins|TrustedInstaller]].
It always has the debug privilege.
