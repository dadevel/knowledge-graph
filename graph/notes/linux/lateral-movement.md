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

# SSH

Login interactively with the password of a domain user trough Kerberos.

~~~ bash
ssh jdoeadm@corp.local@srv01.corp.local
~~~

Pass the ticket to SSH.

~~~ bash
export KRB5CCNAME=./jdoeadm.ccache
ssh jdoeadm@corp.local@srv01.corp.local
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
