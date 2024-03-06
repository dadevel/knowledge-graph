---
title: Credential Phishing with Device Codes
---

[[notes/m365/index]] [[notes/initial-access/credential-phishing]] trough device code authentication.

Authentication flow from victim perspective:

- pick account
- "You're signing in to Microsoft Office on another device located in Germany. If it's not you, close this page."
- "Are you trying to sign in to Microsoft Office? Only continue if you downloaded the app from a store or website that you trust."

For know client IDs see [[notes/entra/foci]].

In the future this login flow can be blocked with [[notes/entra/conditional-access] policies ([source](https://twitter.com/_dirkjan/status/1760966838463111315)), but for now this seems to have some unintended side effects ([source](https://twitter.com/ITguySoCal/status/1762768164910412043)).

Untested tools:

- [DeviceCode2WinHello](https://github.com/kiwids0220/deviceCode2WinHello), persistence with Windows Hello For Business key, see *Phishing for Primary Refresh Tokens and Windows Hello keys* below
- [squarephish](https://github.com/secureworks/squarephish), device code phishing using QR codes
- [PhishInSuits](https://github.com/secureworks/phishinsuits), detailed explanation and implementation with Python script
- [solenya](https://github.com/cultcornholio/solenya), requires to register a new application in the attackers Azure tenant
- [TokenPhisher](https://github.com/CompassSecurity/TokenPhisher) and [TokenTormentor](https://github.com/CompassSecurity/TokenTormentor)

References:

- [Phishing mobile devices, with DeviceCode phishing and QR codes](https://web.archive.org/web/20240116055402/https://badoption.eu/blog/2024/01/08/mobilephish.html), use Azure dev tenant for sending emails, embed QR code in email with UTF8 chars instead of image
- [Evil QR - Phishing With QR Codes](http://web.archive.org/web/20230705155733/https://breakdev.org/evilqr-phishing/)
- [Phishing for Primary Refresh Tokens and Windows Hello keys](http://web.archive.org/web/20231013170658/https://dirkjanm.io/phishing-for-microsoft-entra-primary-refresh-tokens/), use special client id that allows device registration and PRT retrieval
- <https://twitter.com/delivr_to/status/1688506341944356866>, pretext for Microsoft Authenticator
- [Phishing with Azure device codes](https://www.offsec-journey.com/post/phishing-with-azure-device-codes)
- [Abusing family refresh tokens for unauthorized access and persistence in Azure Active Directory](https://github.com/secureworks/family-of-client-ids-research), family refresh tokens from one app also provides access to all other apps in the same family
- [The art of the device code phish](http://web.archive.org/web/20230101165020/https://0xboku.com/2021/07/12/ArtOfDeviceCodePhish.html)
- [New phishing technique: device code authentication](https://o365blog.com/post/phishing/)
