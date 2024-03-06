---
title: Discovery
---

[[notes/mitre-attack/discovery]] in [[notes/entra/index]], [[notes/azure/index]] and [[notes/m365/index]].

Enumerate users, groups and permissions with [[notes/tools/roadtools]].

~~~ bash
roadrecon auth -c 1950a258-227b-4e31-a9cf-717495945fc2 --refresh-token "$(jq -r .refreshToken .roadtools_auth)"
roadrecon gather --mfa  # MFA info requires global reader
roadrecon plugin policies
roadrecon gui
firefox ./caps.html
~~~

Collect info with [[notes/tools/azurehound]] and import the result in [[notes/tools/bloodhound]].
AzureHound uses the Microsoft Azure PowerShell client id (`1950a258-227b-4e31-a9cf-717495945fc2`) internally and requires a matching token.

~~~ bash
roadtx auth -c 1950a258-227b-4e31-a9cf-717495945fc2 ...
azurehound list --refresh-token "$(jq -r .refreshToken .roadtools_auth)" --output ./azurehound.json --tenant corp.com
~~~

Download [PingCastle](https://www.pingcastle.com/download/) and run a scan (currently quite incomplete and not very helpful).

~~~ bat
.\PingCastle.exe --azuread --use-prt
~~~

List group memberships of a user.

~~~ bash
curl -sSf -H "Authorization: Bearer $msgraph_token" 'https://graph.microsoft.com/v1.0/users/VMContributor1@defcorphq.onmicrosoft.com/memberOf' | jq -r '.value[]'
~~~

List which users are assigned what roles on an administrative unit.

~~~ bash
curl -sSf -H "Authorization: Bearer $msgraph_token" "https://graph.microsoft.com/v1.0/directory/administrativeUnits/$unit_id/scopedRoleMembers" | jq -r '.value[]'
curl -sSf -H "Authorization: Bearer $msgraph_token" "https://graph.microsoft.com/v1.0/directoryRoles/$role_id" | jq
~~~
