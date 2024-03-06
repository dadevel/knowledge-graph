---
title: Federation
---

Add a domain for identity federation with ADFS or add an additional token-signing certificate to an existing federated domain to impersonate global admins while bypassing MFA.

References:

- [Meet Silver SAML: Golden SAML in the Cloud](http://web.archive.org/web/20240301192003/https://www.semperis.com/blog/meet-silver-saml/), if you obtained the token signing certificate for a specific service, you can impersonate any user against that service, this is independent from ADFS, implemented in [SilverSamlForger](https://github.com/Semperis/SilverSamlForger)
- [Stealthy Persistence & PrivEsc in Entra ID by using the Federated Auth Secondary Token-signing Cert](http://web.archive.org/web/20240202220007/https://scribe.rip/@cnotin_tenablestealthy-persistence-privesc-in-entra-id-by-using-the-federated-auth-secondary-token-signing-cert-876b21261106)
- [Roles Allowing To Abuse Entra ID Federation for Persistence and Privilege Escalation](https://web.archive.org/web/20240110074906/https://scribe.rip/tenable-techblog/roles-allowing-to-abuse-entra-id-federation-for-persistence-and-privilege-escalation-df9ca6e58360)
- [twitter.com/cnotin/status/1726003826522480985](https://twitter.com/cnotin/status/1726003826522480985)
- [Security vulnerability in Azure AD & Office 365 identity federation](http://web.archive.org/web/20230605210813/https://aadinternals.com/post/federation-vulnerability/)
