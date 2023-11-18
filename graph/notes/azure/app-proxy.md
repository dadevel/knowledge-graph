---
title: Application Proxy
---

> Under construction 🚧

[[notes/azure/index]] Application Proxies allow access to on-prem web apps after authentication to Entra and therefore might allow [[notes/azure/escalation-onprem|lateral movement to on-prem]] if the on-prem app has any vulnerabilities.

Example URL: `https://corpwiki.msappproxy.net`

Application proxies are made of three components:

- Endpoint: user facing external URL
- Application Proxy Service: runs in Azure, passes access token to on-prem connector
- Application Proxy Connector: runs on-prem, communicates with Proxy Service, can leverage Constrained Delegation for apps with Kerberos authentication

As privileged user enumerate applications that have an application proxy configured.

~~~ powershell
Get-AzureADApplication | %{try {Get-AzureADApplicationProxyApplication -ObjectId $_.ObjectID;$_.DisplayName;$_.ObjectID} catch {}}
~~~

Find users and groups assigned to the application as privileged user.

~~~ powershell
Get-AzureADServicePrincipal -All $true | ?{$_.DisplayName -eq "Finance Management System"}
Import-Module .\Get-ApplicationProxyAssignedUsersAndGroups.ps1
Get-ApplicationProxyAssignedUsersAndGroups -ObjectId $service_principal_guid
~~~
