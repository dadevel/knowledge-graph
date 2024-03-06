---
title: NTLM Relay between MSSQL Servers
---

Relay the service account from one [[notes/ad/mssql]] server to another.

Search for MSSQL servers with guest access that run under a domain account (no `NT Service` under `Service Account`).

=== "[[notes/tools/powerupsql]]"
    ~~~ powershell
    Get-SQLInstanceDomain | Get-SQLServerInfo -Verbose
    ~~~

[[notes/ad/ntlm-relay-from-mssql|Coerce authentication from MSSQL servers]] and [[notes/ad/ntlm-relay-to-smb]] or [[notes/ad/ntlm-relay-to-mssql]] on other MSSQL servers.
