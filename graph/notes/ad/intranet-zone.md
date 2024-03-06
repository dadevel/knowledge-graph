---
title: Intranet Zone
---

Windows allows NTLM authentication over HTTP only on domains it considers to be on the intranet.
Firefox always prompts the user for credentials even on the intranet.

During local privilege escalation this can be achieved by redirecting ports from localhost.

Otherwise you have the following options:

- use the hostname of an owned machine
- register a hostname for your IP via [[notes/ad/adidns-spoofing|ADIDNS]], this can even be a public IP somewhere on the internet
- advertise a hostname in the local subnet via [[notes/network/llmnr-mdns-nbt-ns-spoofing]] ([source](https://gist.github.com/gladiatx0r/1ffe59031d42c08603a3bde0ff678feb))
- buy your own TLD, public domains without dots are considered intranet ([source](https://twitter.com/wdormann/status/1639255276762148866))

Test if an UNC path is considered internet (3) or intranet (0) with [MapUrlToZone()](https://gist.github.com/HumanEquivalentUnit/9756f97bc67d2a0807993c05e426a436).

ADIDNS might contain additional trusted domains that can be abused ([source](https://twitter.com/SwiftOnSecurity/status/1683586301088391169)).

Create a DNS record for `mysubdomain.corp.local`.
After this is replicated to the other domain controllers, `mysubdomain` belongs to the intranet.

=== "[[notes/tools/krbrelayx]]"
    ~~~ bash
    krbrelayx-dnstool -u 'corp.local\jdoe' -p 'passw0rd' -a add -r mysubdomain -d 192.0.2.1 dc01.corp.local
    ~~~
