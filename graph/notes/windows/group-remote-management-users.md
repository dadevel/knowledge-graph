---
title: Remote Management Users Group
---

*Remote Management Users* / *Remoteverwaltungsbenutzer* is one of the [[notes/windows/high-value-groups]] because members can login via [[notes/network/winrm]].

Find WinRM endpoints where *Remote Management Users* have access.

~~~ powershell
Get-PSSessionConfiguration | where {$_.Permission -match 'Remote Management Users'}
~~~

References:

- [Poc'ing beyond Domain Admin - Part 1](http://web.archive.org/web/20230129100526/https://cube0x0.github.io/Pocing-Beyond-DA/)
