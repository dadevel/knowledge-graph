---
title: SeBackupPrivilege
---

A [[notes/windows/privilege]] that allows escalation to local admin, because you can access arbitrary files.

Copy a directory.

=== "builtin"
    ~~~ bat
    robocopy.exe /b /e C:\Users\Administrator\Desktop\ C:\temp\
    ~~~

Untested tools:

- [SeBackupPrivilegePoC](https://github.com/daem0nc0re/PrivFu/blob/main/PrivilegedOperations/SeBackupPrivilegePoC)
- [BackupOperators.cpp](https://github.com/Wh04m1001/Random/blob/main/BackupOperators.cpp), can copy registry hives
- [SeBackupPrivilegeCmdLets](https://github.com/giuliano108/SeBackupPrivilege)

References:

- [Poc'ing beyond Domain Admin - Part 1](http://web.archive.org/web/20230129100526/https://cube0x0.github.io/Pocing-Beyond-DA/)
- [Windows PrivEsc with SeBackupPrivilege](http://web.archive.org/web/20230113234215/https://scribe.rip/@nairuzabulhul/windows-privesc-with-sebackupprivilege-65d2cd1eb960)
