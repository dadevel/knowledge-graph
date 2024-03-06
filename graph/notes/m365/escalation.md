---
title: M365 Escalation
---

Dangerous permissions (app roles) for Microsoft Graph:

- `RoleManagement.ReadWrite.Directory`: service principal can grant itself any Entra ID role, including *Global Administrator* ([source](http://web.archive.org/web/20240204091719/https://scribe.rip/@specterops/azure-privilege-escalation-via-azure-api-permissions-abuse-74aee1006f48))
- `AppRoleAssignment.ReadWrite.All`: service principal can grant itself any app role and bypass the consent process ([source](http://web.archive.org/web/20240204091719/https://scribe.rip/@specterops/azure-privilege-escalation-via-azure-api-permissions-abuse-74aee1006f48))
- `Application.ReadWrite.All`: service principal can add credential to other application
- `Group.ReadWrite.All`: add owners and members to non-role-assignable groups
- `GroupMember.ReadWrite.All`: add members to non-role-assignable groups
- `ServicePrincipalEndpoint.ReadWrite.All`: add credentials to existing service principals
- `User.ReadWrite.All`: hijack user by editing `otherMail` attribute to convert account to B2B user, fixed?
- `User.Invite.All` + `User.ManageIdentities.All`: hijack user by adding B2B identity to target user, fixed?
- `Policy.ReadWrite.AuthenticationMethod` + `Organization.ReadWrite.All`: configure certificate-based authentication for organization ([source](http://web.archive.org/web/20221222100649/https://scribe.rip/@specterops/passwordless-persistence-and-privilege-escalation-in-azure-98a01310be3f))
- `Policy.ReadWrite.AuthenticationMethod` + `UserAuthenticationMethod.ReadWrite.All`: configure [[notes/entra/tap]] for user
- `Directory.ReadWrite.All`: add member to non-role-assignable security group, add owner to non-role-assignable security group, add user to the tenant ([source](http://web.archive.org/web/20240214203255/https://scribe.rip/@spectreops/directory-readwrite-all-is-not-as-powerful-as-you-might-think-c5b09a8f78a8))

References:

- [twitter.com/cnotin/status/1751045526919819320](https://twitter.com/cnotin/status/1751045526919819320), Microsoft Midnight Blizzard breach
- [How to grant admin consent to an API programmatically](http://web.archive.org/web/20240204134340/https://scribe.rip/@MalikSahil/how-to-grant-admin-consent-to-an-api-programmatically-e32f4a100e9d)
- [Microsoft Graph Permission Explorer](https://graphpermissions.merill.net/permission/index.html), explanation of all MS Graph permissions
- [AbuseAzureAPIPermissions](https://github.com/Hagrid29/AbuseAzureAPIPermissions), abusable MS Graph permissions
