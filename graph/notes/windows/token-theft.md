---
title: Token Theft
---

Dump access tokens from process memory of Microsoft Office, Teams, OneDrive or other SaaS products as unprivileged user.

The log files in `%localappdata%\Microsoft\Olk\EBWebView\Default\Session Storage` might contain O365 refresh tokens ([source](https://twitter.com/__Retrospect/status/1742929451523117325)).

Untested tools:

- [AzTokenFinder](https://github.com/hackmichnet/aztokenfinder), extracts strings from process memory that look like JWTs
- [WAMBam](https://github.com/xpn/WAMBam)

References:

- [Converting Tokens to Session Cookies for Outlook Web Application](http://web.archive.org/web/20230831082935/https://labs.lares.com/owa-cap-bypass/)
- [Bypassing Microsoft Token Protection](http://web.archive.org/web/20230512204359/https://scribe.rip/@rootsecdev/bypassing-microsoft-token-protection-c176328d4120), token protection can be bypassed by posing as MacOS device
- [Stealing access tokens from Office desktop applications](http://web.archive.org/web/20220919231117/https://mrd0x.com/stealing-tokens-from-office-applications/)
- [WAM BAM - Recovering web tokens from Office](http://web.archive.org/web/20230129100506/https://blog.xpnsec.com/wam-bam/)
