---
title: NTLM Relaying
---

[[notes/ad/escalation]] trough NTLM Relaying.

![NTLM relay techniques ([source](https://www.thehacker.recipes/ad/movement/ntlm/relay))](https://3210236927-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F-MHRw3PMJtbDDjbxm5ub%2Fuploads%2FMEMuGPBPviYyGAQfwdqp%2FNTLM%20relay.png?alt=media&token=554b6390-8f85-4d35-8fcc-7b5aa32f2933)

General Steps:

1. Coerce a [[notes/ad/ntlm-relay-source]] to authenticate to your system
2. Forward incoming authentication request from your system to a [[notes/ad/ntlm-relay-sink]]

As rule of thumb [[notes/ad/ntlm-relay-from-smb|SMB]] can be relayed everywhere with [[notes/ad/ntlmv1]] and with [[notes/ad/ntlmv2]] only to [[notes/ad/ntlm-relay-to-smb|SMB]] and [[notes/ad/ntlm-relay-to-http|HTTP]].
[[notes/ad/ntlm-relay-from-http|HTTP]] can be relayed everywhere, including [[notes/ad/ntlm-relay-to-ldap|LDAP]].
Source and sink must always be different systems.

> **Note:** If `impacket-ntlmrelayx` fails to forward an incoming authentication request with `Unsupported MechType 'NEGOEX - SPNEGO Extended Negotiation Security Mechanism'`, the source is probably a Linux system running Samba.

References:

- [en.hackndo.com/ntlm-relay](https://en.hackndo.com/ntlm-relay/)
- [thehacker.recipes/ad/movement/ntlm/relay](https://www.thehacker.recipes/ad/movement/ntlm/relay)
- [Coercions and relays - The first cred is the deepest with Gabriel Prud'homme](https://www.youtube.com/watch?v=b0lLxLJKaRs), demos of many different attack techniques
- [Relaying 101](http://web.archive.org/web/20230101182056/https://luemmelsec.github.io/Relaying-101/)
- [A comprehensive guide to relaying anno 2022](http://web.archive.org/web/20221006094955/https://www.trustedsec.com/blog/a-comprehensive-guide-on-relaying-anno-2022/)
- [Examples for SOCKS proxy feature of ntlmrelayx](https://www.secureauth.com/blog/playing-with-relayed-credentials/)
