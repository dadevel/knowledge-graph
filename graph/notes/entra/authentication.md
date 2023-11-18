---
title: Authentication
---

Authentication methods for [[notes/entra/index]].

Sign in interactively in your browser via the device code flow.

~~~ bash
roadtx auth -c azps -r msrgaph -t corp.com --device-code
~~~

Device code authentication by hand.

~~~ bash
curl -sSf 'https://login.microsoftonline.com/common/oauth2/devicecode?api-version=1.0' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36' -d client_id=1950a258-227b-4e31-a9cf-717495945fc2 -d resource=https://graph.microsoft.com
firefox https://microsoft.com/devicelogin
curl -sSf 'https://login.microsoftonline.com/Common/oauth2/token?api-version=1.0' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36' -d client_id=1950a258-227b-4e31-a9cf-717495945fc2 -d grant_type=urn:ietf:params:oauth:grant-type:device_code -d code=$code
~~~

Sign in using an existing refresh token (client ID must be provided explicitly).

~~~ bash
roadtx auth -c azps --refresh-token '0.AQsAH...'
~~~

Use Azure CLI as service principal.

~~~ bash
az login --service-principal --allow-no-subscriptions -u $client_id -p $pass_or_cert --tenant $tenant_id
~~~

Pass an access token with `User.ReadBasic.All` to Microsoft Graph to get a list of all users.

~~~ bash
curl -sSf 'https://graph.microsoft.com/v1.0/users' -H "Authorization: Bearer $msgraph_token" | jq
~~~

Get the client id of an existing token.

~~~ bash
roadtx describe < .roadtools_auth | jq -r '.appid' | tail -n 1
~~~

For a list of Microsoft public clients see [microsoft-public-clients.csv](./microsoft-public-clients.csv) ([source](https://github.com/emiliensocchi/azure-hunting/blob/master/Miscellaneous/Public%20client%20applications.md)).

Also see [[notes/entra/foci]] and [[notes/entra/device-registration]].

Untested tools:

- [TokenMan](https://github.com/secureworks/tokenman), turns refresh token into authentication files for `az` CLI

References:

- [jwt.ms](https://jwt.ms/), official JWT decoder
- [Going passwordless with Window Hello for Business and SCRIL](http://web.archive.org/web/20230522081555/https://cloudbrothers.info/en/going-passwordless-whfb-scril/)

# Single Sign-On

Single Sign-On automatically signs users in to cloud-based apps when they use their corporate devices (hybrid or Azure-joined).
It can be implemented with legacy [[notes/entra/ssso]] or based on [[notes/entra/prt|PRTs]].

# Privileged Identity Management

Existing tokens are not invalidated when you PIM.
The token can be stolen before PIM and used after the role has been activated ([source](https://twitter.com/miketheitguy/status/1703597245671907797)).

# Continuous Access Evaluation

Continuous Access Evaluation can invalidate access tokens before their default expiry time of 1h.
It blocks the use of access token outside of trusted locations when location based conditional access is present.
In CAE sessions the access token lifetime is increased up to 28h.

CAE needs explicit client support which is currently only present in the most common Microsoft products.
If an access token contains `"xms_cc":["CP1"]` the client that obtained it supports CAE.

CAE steps in when the following events occur:

- account disabled or deleted
- password change or reset
- MFA enabled
- refresh token revoked
- high user risk detected by Azure AD identity Protection
- IP-based named location
