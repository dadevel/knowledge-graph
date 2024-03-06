---
title: NTLM Relay between Computers
---

If computer A is `AdminTo` computer B you can [[notes/ad/ntlm-relay-from-smb|coerce NTLM authentication over SMB]] from A and [[notes/ad/ntlm-relay-to-smb|relay over SMB]] to B ([source](https://twitter.com/n00py1/status/1574426163010740225)).
This is quite common with [[notes/network/microsoft-exchange]] servers.
Check the edges of the *Exchange Trusted Subsystem* group in [[notes/tools/bloodhound]].
