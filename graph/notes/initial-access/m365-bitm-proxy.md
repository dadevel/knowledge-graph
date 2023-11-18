---
title: Credential Phishing with BitM Proxy
---

[[notes/m365/index]] [[notes/initial-access/index]] by phishing credentials and session cookies trough a Browser in the Middle proxy.

Instead of proxying HTTP requests like with a [[notes/initial-access/m365-aitm-proxy|AitM Proxy]], this technique forwards user input to a remote browser and shows the result to the user.

[[notes/entra/conditional-access|CAPs]] that require phishing resistant authentication or device compliance prevent this attack ([source](https://www.youtube.com/watch?app=desktop&v=tI1bdVohOK8)).

Untested tools:

- [cuddlephish](https://github.com/fkasler/cuddlephish), forwards user input to remote Chrome instance, sends video stream back
- [phishim](https://github.com/jackmichalak/phishim), forwards user input to remote Chrome instance, sends screenshots back

References:

- [MFA Phishing using noVNC and AWS](http://web.archive.org/web/20230221150751/https://scribe.rip/@psychsecurity/mfa-phishing-using-novnc-and-aws-ebc781b4d093)
