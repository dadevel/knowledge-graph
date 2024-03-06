---
title: Local Privilege Escalation as Network Service
---

Local [[notes/windows/escalation]] from a virtual service account or *NT Authority/Network Service* to admin without abusing [[notes/windows/privilege|privileges]].

A) Obtain a TGT for the computer account trough [[notes/windows/kerberos-dump|TGT Delegation]].
Then impersonate an admin against the computer with [[notes/ad/kerberos-delegate2thyself]] ([source](./roses-are-red-violets-are-blue-s4u-bamboozles-me-u2u-too-charlie-bromberg-northsec-2023.pdf)).

B) [[notes/ad/adcs-certificate-request|Request a machine certificate]] from ADCS, [[notes/ad/unpac-the-hash]] and forge a [[notes/ad/silver-ticket]] ([source](http://web.archive.org/web/20221207065918/https://sensepost.com/blog/2022/certpotato-using-adcs-to-privesc-from-virtual-and-network-service-accounts-to-local-system/)).

Untested tools:

- [S4UTomato](https://github.com/wh0amitz/S4UTomato), automates the TGT Delegation trick, also supports RBCD and Shadow Credentials
- [SharpToken](https://github.com/BeichenDream/SharpToken/tree/main#elevated-permissions), steal `NT AUTHORITY\SYSTEM` token as `NT AUTHORITY\NETWORK SERVICE`, see [Sharing a Logon Session a Little Too Much](https://web.archive.org/web/20240128225939/https://www.tiraniddo.dev/2020/04/sharing-logon-session-little-too-much.html)
