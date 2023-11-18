---
title: FOCI
---

The Family of Client IDs (FOCI) is a group of Microsoft applications like Office, Outlook and Teams where the refresh token of one client can be used to gain a refresh token for any other client in the group.
So a refresh token from Azure CLI can be turned into an refresh token for Outlook and subsequently used to read emails.

For example refresh to Microsoft Office with [[notes/tools/roadtools]].

~~~ bash
roadtx auth --tokens-stdout --client d3590ed6-52b3-4102-aeff-aad2292ab01c --tenant corp.com --resource msgraph --refresh-token $refreshtoken
~~~

For a list of known clients that are part of FOCI check [foci.csv](./foci.csv).

Find Microsoft clients that have a specific permission.
You can also check out [this table](https://github.com/secureworks/family-of-client-ids-research/blob/main/scope-map.txt).

~~~ bash
roadtx getscope -s https://graph.microsoft.com/mail.read
~~~

References:

- [Application IDs of commonly used Microsoft applications](https://learn.microsoft.com/en-us/troubleshoot/azure/active-directory/verify-first-party-apps-sign-in#application-ids-of-commonly-used-microsoft-applications)
- [TROOPERS22: Abusing family refresh tokens for unauthorized access and persistence in Azure AD](https://www.youtube.com/watch?v=fTLzi9GCfBA)
- [Family of client IDs research](https://github.com/secureworks/family-of-client-ids-research)
