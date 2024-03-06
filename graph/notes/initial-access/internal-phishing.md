---
title: Internal Phishing
---

Attachments on emails send from internal domains are not tagged with [[notes/infection/motw]] ([source](https://web.archive.org/web/20231206161457/https://research.checkpoint.com/2023/the-obvious-the-normal-and-the-advanced-a-comprehensive-analysis-of-outlook-attack-vectors/)).
This makes office documents with macros viable again.
Additionally it is possible to coerce NTLM authentication trough links to internal domains.

References:

- [Insecure comments](http://web.archive.org/web/20221012071137/https://scribe.rip/@mearegtu/insecure-comments-73399193f804), M365 Word and PowerPoint allow an unprivileged user to add comments to documents he/she has write access to as an arbitrary other user
