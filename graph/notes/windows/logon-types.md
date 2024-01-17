---
title: Logon Types
---

Name                      | Number | Cached | Description
--------------------------|--------|--------|------------
System                    | 0      | na     | used by system at start up
Interactive               | 2      | yes    | local authentication with password
Network                   | 3      | no     | remote authentication via Kerberos or NTLM, e.g. WinRM
Batch                     | 4      | yes    | used by scheduled tasks
Service                   | 5      | yes    | used by services
Proxy                     | 6      | ?      | ?
Unlock                    | 7      | yes    | user with physical presence unlocks machine
Network Cleartext         | 8      | no     | remote authentication with password, e.g. OpenSSH
New Credentials           | 9      | yes    | used by `runas /netonly`
Remote Interactive        | 10     | yes    | remote authentication with password, e.g. RDP
Cached Interactive        | 11     | ?      | local authentication against cached credentials
Cached Remote Interactiev | 12     | ?      | remote authentication against cached credentials
Cached Unlock             | 13     | ?      | local authentication against cached credentials

# Caching Behavior

Action                      | LogonType | Cached | Notes
----------------------------|-----------|--------|------
Console Logon               | 2         | yes    | except when Credential Guard is enabled
RunAs                       | 2         | yes    | except when Credential Guard is enabled
PsExec with explicit creds  | 2 + 3     | yes    |
PsExec wo. explicit creds   | 3         | no     |
Remote Registry             | 3         | no     |
SMB Share                   | 3         | no     |
WMI                         | 3         | no     |
WinRM & PowerShell Remoting | 3         | no     |
Scheduled Task              | 4         | yes    | password saved as LSA secret
Service                     | 5         | yes    | password saved as LSA secret
FTP                         | 8         | no     |
IIS Basic Auth              | 8         | no     |
SSH                         | 8         | no     |
RDP                         | 10        | yes    | except when Remote Credential Guard is enabled

References:

- [Fantastic Windows Logon types and Where to Find Credentials in Them](https://web.archive.org/web/20230728212559/https://www.alteredsecurity.com/post/fantastic-windows-logon-types-and-where-to-find-credentials-in-them)
- [Administrative tools and logon types](https://learn.microsoft.com/en-us/windows-server/identity/securing-privileged-access/reference-tools-logon-types)
