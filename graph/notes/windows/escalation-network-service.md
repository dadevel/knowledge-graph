---
title: Local Privilege Escalation as Network Service
---

Local [[notes/windows/escalation]] from a virtual service account or *NT Authority/Network Service* to admin without abusing [[notes/windows/privilege|privileges]].

First obtain a TGT for the computer account trough [[notes/windows/kerberos-dump|TGT Delegation]].
Then impersonate an admin against the computer with [[notes/ad/delegate2thyself]] ([source](./roses-are-red-violets-are-blue-s4u-bamboozles-me-u2u-too-charlie-bromberg-northsec-2023.pdf)).

Untested tools:

- [S4UTomato](https://github.com/wh0amitz/S4UTomato), automates the TGT Delegation trick, also supports RBCD and Shadow Credentials
- [SharpToken](https://github.com/BeichenDream/SharpToken/tree/main#elevated-permissions), steal `NT AUTHORITY\SYSTEM` token as `NT AUTHORITY\NETWORK SERVICE`
