---
title: Process Integrity
---

[[notes/windows/index]] process integrity levels:

- System integrity: `NT Authority\System`
- High integrity: administrators
- Medium integrity: standard users, administrators with filtered token
- Low integrity: restricted rights, sandboxed processes

A process with lower integrity level can not modify a process of higher integrity level.
Additionally a [[notes/windows/ppl|PPL]] process can not be modified by a non-PPL process.

Local administrators have a medium integrity token by default and can elevate to high integrity trough [[notes/windows/uac-bypass|UAC]].

# Discovery

The integrity level is displayed at the bottom and named `Mandatory Level`.

~~~ bat
whoami.exe /groups
~~~
