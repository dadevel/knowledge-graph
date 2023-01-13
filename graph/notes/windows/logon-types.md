---
title: Logon Types
---

Name | Number | Cached | Description
-----|--------|--------|------------
Interactive | 2 | yes | Local authentication with plain password
Network | 3 | no |
Batch | 4 | yes | used by scheduled tasks
Service | 5 | yes | used by services
Unlock | 7 | yes | User with physical presence unlocks machine
Network Cleartext | 8 | no |
New Credentials | 9 | yes | used by `runas`
Remote Interactive | 10 | yes | Remote authentication with plain password, e.g. over RDP
Cached Interactiev | 11 | yes |

# Caching Behavior

Action                    | LogonType | Cached | Notes
--------------------------|-----------|--------|------
console logon             | 2         | yes    | except when Credential Guard is enabled
RunAs                     | 2         | yes    | except when Credential Guard is enabled
RDP                       | 10        | yes    | except when Remote Credential Guard is enabled
net use                   | 3         | no     |
PowerShell Remoting       | 3         | no     | e.g. `Invoke-Command`, `Enter-PSSession`
PsExec alternate creds    | 3 + 2     | yes    |
PsExec wo. explicit creds | 3         | no     |
Remote Scheduled Task     | 4         | yes    | password saved as LSA secret
Run as service            | 5         | yes    | password saved as LSA secret
Remote Registry           | 3         | no     |

References:

- SANS 508
- [Administrative tools and logon types](https://learn.microsoft.com/en-us/windows-server/identity/securing-privileged-access/reference-tools-logon-types)
