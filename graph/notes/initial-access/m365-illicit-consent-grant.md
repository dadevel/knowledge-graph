---
title: Credential Phishing trough Illicit Consent Grant
---

[[notes/m365/index]] [[notes/initial-access/index]] trough phishing refresh tokens with a malicious multi tenant app.

There are three standard consent policies:

Consent policy                                          | Description
--------------------------------------------------------|------------
Do not allow user consent                               | allows no apps
Allow user consent for apps from verified publishers    | allows low impact permissions for apps from same tenant and verified publishers
Allow user consents for all apps (default?)              | allows apps from other tenants and unverified publishers

Permissions that are considered low impact by default: `openid`, `profile`, `email`, `offline_access`, `User.Read`, `User.ReadBasic.All` (name and email of all users in tenant)

All other permissions require admin consent and can only be used when phishing privileged users (e.g. with *Application Administrator* role).
Interesting permissions are: `Mail.Read`, `Mail.Send`, `Mailboxsettings.ReadWrite`, `Files.ReadWrite.All`, `Notes.Read.All`

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
