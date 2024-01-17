---
title: LSA Proxy
---

Really cool concept, but could not get it to work :(

Start [wsnet-dotnet](https://github.com/skelsec/wsnet-dotnet) on the victim machine (binds to port 8700 by default).

~~~ bat
.\WSNetFramework.exe
~~~

Run SMB client with [wsnet](https://github.com/skelsec/wsnet) integration on the attacker machine.

~~~ bash
asmbclient -v 'smb2+wsnetdirect-ntlm://ws01\jdoe@172.30.253.2/?proxytype=wsnetdirect&proxyhost=172.30.253.2&proxyport=8700&wsip=172.30.253.2'
~~~

References:

- [Spooky Authentication at a Distance - Tamas Jos - DEF CON 31](https://www.youtube.com/watch?v=7oAZK8x_mL0)
