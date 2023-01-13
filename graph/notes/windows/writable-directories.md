---
title: Writable Windows Directories
---

Globally writable directories on [[notes/windows/index]].

~~~
%APPDATA%
%TEMP%
%USERPROFILE%
C:\Users\Public
C:\Windows\Registration\CRMLog
C:\Windows\System32\FxsTmp
C:\Windows\System32\Microsoft\Crypto\RSA\MachineKeys
C:\Windows\System32\Tasks
C:\Windows\System32\Tasks\Microsoft\Windows\PLA\System
C:\Windows\System32\Tasks\Microsoft\Windows\SyncCenter
C:\Windows\System32\Tasks_Migrated
C:\Windows\System32\com\dmp
C:\Windows\System32\spool\PRINTERS
C:\Windows\System32\spool\SERVERS
C:\Windows\System32\spool\drivers\color
C:\Windows\Tasks
C:\Windows\Temp
C:\Windows\servicing\Packages
C:\Windows\servicing\Sessions
C:\Windows\tracing
~~~

You can also try `C:\Windows\Sysnative` or `C:\Windows\SysWOW64` instead of `C:\Windows\System32`.

Find additional directories with [accesschk](https://learn.microsoft.com/en-us/sysinternals/downloads/accesschk).

~~~ bat
.\accesschk.exe -accepteula -nobanner -w -u -s %USERNAME% C:\
~~~
