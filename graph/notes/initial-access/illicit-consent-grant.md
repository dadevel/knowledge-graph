---
title: Credential Phishing trough Illicit Consent Grant
---

[[notes/m365/index]] [[notes/initial-access/credential-phishing]] by gaining refresh tokens trough a malicious multi tenant app.

There are three standard consent policies:

Consent policy                                          | Description
--------------------------------------------------------|------------
Do not allow user consent                               | only admins can consent
Allow user consent for apps from verified publishers    | allows consent to apps from verified third-party publishers or apps in the same tenant, new default
Allow user consents for all apps                        | allows consent to apps from unverified publishers, old default

By default users can grant third-party apps the permissions `openid`, `profile`, `email`, `offline_access`, `User.Read` and `User.ReadBasic.All` (name and email of all users in tenant).
All other permissions require admin consent.

Furthermore users can create app registrations in their tenant and can grant risky permissions like `Chat.ReadWrite`, `ChatMessage.Send`, `Files.ReadWrite.All` `Mail.ReadWrite`, `Mail.Send`, `MailboxSettings.ReadWrite`, and `Notes.Read.All`, `Site.Read.All`, `Tasks.Read.Shared`, `User.ReadWrite` to this first-party apps.
This can be abused during internal phishing ([source](https://twitter.com/EricaZelic/status/1753642752124883400), [source](https://twitter.com/EricaZelic/status/1753841848131453147)).

Check the consent policy as authenticated user.

~~~ bash
curl -sSf -H "Authorization: Bearer $msgraph_token" 'https://graph.microsoft.com/v1.0/policies/authorizationPolicy' | jq -r '.allowUserConsentForRiskyApps'
~~~

To setup an app for consent grant phishing follow this steps:

- open [portal.azure.com](https://portal.azure.com/) in your attacker tenant, click *App registrations*, click *New registration*, give a name, under *Supported account types* select *Accounts in any organization* and provide a redirect URI to a server you control
- go to *Certificates & secrets* and *New client secret*
- go to *API permissions*, *Add a permission* and add following delegated permissions for Microsoft Graph: `User.Read`, `User.ReadBasic.All`

Other tools:

- [365-Stealer](https://github.com/AlteredSecurity/365-Stealer), not intended for production

Untested tools:

- [o365-attack-toolkit](https://github.com/mdsecactivebreach/o365-attack-toolkit)
- [Vajra](https://github.com/TROUBLE-1/Vajra)
