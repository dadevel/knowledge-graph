---
title: Credential Phishing with AitM Proxy
---

[[notes/m365/index]] [[notes/initial-access/index]] by phishing credentials and session cookies trough an Attacker in the Middle proxy.

Some websites like Google and LinkedIn try to prevent AitM phishing by delivering obfuscated JavaScript that validates the domain, e.g. via `window.location` or `document.location` ([source](https://drive.google.com/file/d/1zZIZta5wa1U-bHp66sH42xVdyVkjkr2L/view)).
Currently Microsoft does not deploy such countermeasures.
In any case this checks can be circumvented by using a [[notes/initial-access/m365-bitm-proxy|BitM Proxy]] instead.

[[notes/entra/conditional-access|CAPs]] that require phishing resistant authentication prevent this attack ([source](https://www.youtube.com/watch?app=desktop&v=tI1bdVohOK8)).

Exchange a phished Azure `ESTSAUTHPERSISTENT` cookie for an access token ([source](https://twitter.com/_dirkjan/status/1666883269671911455)).

=== "[[notes/tools/roadtools]]"
    ~~~ bash
    roadtx interactiveauth --estscookie 0.AXQA...
    ~~~

Other tools:

- [evilginx2](https://github.com/kgretzky/evilginx2), written in Go, requires separate domain because of mandatory integrated DNS server
  - additional templates in [Evilginx3-Phishlets](https://github.com/simplerhacking/Evilginx3-Phishlets)
- [Modlishka](https://github.com/drk1wi/modlishka), written in Go, no DNS management
- [Muraena](https://github.com/muraenateam/muraena), written in Go, no DNS management, can be combined with [necrobrowser](https://github.com/muraenateam/necrobrowser)

References:

- [How to protect against modern phishing attacks like Evilginx](https://web.archive.org/web/20231202043908/https://bleekseeks.com/blog/how-to-protect-against-modern-phishing-attacks)
- [The Triforce of Initial Access](http://web.archive.org/web/20231109132519/https://trustedsec.com/blog/the-triforce-of-initial-access), combination of EvilGinx, ROADtools and TeamFiltration
- [Hook, Line, and Phishlet: Conquering AD FS with Evilginx](http://web.archive.org/web/20230803165950/https://research.aurainfosec.io/pentest/hook-line-and-phishlet/)
- [AiTM/MFA phishing attacks in combination with new Microsoft protections (2023 edition)](http://web.archive.org/web/20230705062639/https://jeffreyappel.nl/aitm-mfa-phishing-attacks-in-combination-with-new-microsoft-protections-2023-edt/)
- [Browser in the browser attack](http://web.archive.org/web/20221006095538/https://mrd0x.com/browser-in-the-browser-phishing-attack/)
