---
title: Conditional Access
---

# Theory

- *Conditional Access Policies* (CAPs) don't work like firewall rules, all conditions must be satisfied ([source](https://twitter.com/lukasberancz/status/1651934975074222082))
- *Condition*: error before MFA prompt
- *Access Control*: error after MFA prompt (MFA itself is an *Access Control*)
- *Client Application*
    - Modern authentication clients
        - Browser
        - Native (mobile apps and desktop clients)
    - Legacy authentication clients
        - Exchange ActiveSync
        - Other (POP3, IMAP, SMTP)

Authentication errors explained ([source](https://web.archive.org/web/20220923201435/https://danielchronlund.com/2022/01/07/the-attackers-guide-to-azure-ad-conditional-access/)):

Error | Type | Reason
------|------|-------
We've detected suspicious activity on your account | condition | sign-in risk | use VPN close to victims physical location
Your sign-in was successful but does not meet the criteria to access this resource | condition | device platform, location or client app restriction | fake `User-Agent` header, use VPN, use browser or fake AAD-joined device
This application [...] can only be accessed from [...] domain joined devices | access control | require hybrid-joined device | try to fake AAD-joined device
This application [...] can only be accessed from [...] devices [...] that meet the management compliance policy | access control | require Intune-compliant device | try to fake Intune compliance

References:

- [An Azure Tale of VPN, Conditional Access and MFA Bypass](http://web.archive.org/web/20230815182930/https://simondotsh.com/infosec/2023/08/15/azure-tale-vpn-ca-mfa-bypass.html), practical example of MFA bypass trough weak CAPs

# Practice

Generate list of CAPs from [[notes/tools/roadtools]] ([source](https://www.youtube.com/watch?v=SK1zgqaAZ2E&t=11m30s)).

~~~ bash
roadrecon plugin policies
firefox ./caps.html
~~~

Dump raw CAPs.

~~~ bash
curl -sSf -H "Authorization: Bearer $msgraph_token" 'https://graph.microsoft.com/v1.0/identity/conditionalaccess/policies' | jq
~~~

Analyze CAPs with [caOptics](https://github.com/jsa2/caOptics) as Security Reader or Global Reader.
The CSV report can be imported back into [[notes/tools/roadtools]] with [PR 61](https://github.com/dirkjanm/ROADtools/pull/61).

~~~ bash
git clone --depth 1 https://github.com/jsa2/caoptics
cd ./caoptics
podman run -it --rm --network host -v .:/workdir -w /workdir --entrypoint bash docker.io/library/node:14
npm install
node ./ca/main.js --mapping --clearPolicyCache --clearTokenCache --clearMappingCache
~~~

# Bypasses

## Recently Recruited Employee

Just try to authenticate, maybe you are lucky and your user hasn't enrolled MFA yet.

As authenticated user you can search for accounts where the creation and password change date are equal.
This is a strong indicator that they don't yet have MFA enrolled.

Untested tools:

- [Azure-AD-Password-Checker](https://github.com/quahac/Azure-AD-Password-Checker)

## Excluded Device Platforms

If MFA is not enforced for all device platforms, it can be easily bypassed by forging the `User-Agent` HTTP header.
For example Microsofts official template excludes Linux systems ([source](https://twitter.com/rootsecdev/status/1682369951640715264)).

## Excluded Users

MFA is not enforced for all users.
Maybe your user is member of a group that is excluded.
This is often the case for service accounts.

## Excluded Applications

MFA might not be enforced for all apps.
Try MS Graph or 3rd party SaaS integrations.

## Excluded Locations

Requests from *Trusted Locations* (countries or specific subnets) can be exempt from MFA.
This might include the guest WiFi.

## Excluded Clients

MFA might not be enforced for all clients.
For example Microsofts *Security Defaults* policy excludes Microsoft Graph unless legacy per user MFA is enabled ([source](http://web.archive.org/web/20230901192937/https://scribe.rip/@rootsecdev/azure-ad-security-defaults-mfa-bypass-with-graph-api-86a5d6f57d4a)).

## Legacy Authentication

Check with [MFASweep](https://github.com/dafthack/mfasweep).

~~~ powershell
Import-Module .\MFASweep.ps1
Invoke-MFASweep -username somebody@corp.onmicrosoft.com -password passw0rd
~~~

## Other SaaS Apps

Find out which SaaS offerings an organization is using.
Maybe one of them does not required MFA ([source](https://twitter.com/EricaZelic/status/1640054683711438848)).
Or it isn't connect to AAD at all and the user reuses his/her password.

## OAuth Resource Owner Password Credentials

Audit: Find applications that can bypass MFA trough the ROPC OAuth flow.

~~~
./ropci configure
./ropci auth devicecode
./ropci apps list --all --format json | jq -r '.value[]|[.displayName,.appId]|@csv' > ./apps.csv
./ropci auth bulk -i ./apps.csv -o ./results.json --verbose
jq -r 'select(.access_token!="")|[.display_name,.scope]|@csv' ./results.json
~~~

References:

- [ROPC - So, you think you have MFA?](http://web.archive.org/web/20231026151608/https://embracethered.com/blog/posts/2022/ropci-so-you-think-you-have-mfa-azure-ad/)

## On-prem Services

Exchange/OWA and other websites that use NTLM-based authentication don't support MFA.

## Additional Tenants

Open [portal.azure.com/b2c.aadinternals.com](https://portal.azure.com/b2c.aadinternals.com), login with username and password (no MFA required), click on your profile in the top right corner and select *switch tenant* to get a list of all tenants the user can access ([source](http://web.archive.org/web/20230909011032/https://aadinternals.com/talks/Abusing%20Azure%20Active%20Directory.%20From%20MFA%20Bypass%20to%20Listing%20Global%20Administrators.pdf)).
Test if any tenant is vulnerable to one of the misconfigurations described above.

This is possible because home tenant admins can't block access to resource tenants and resource tenant admins can choose to not enforce home tenant MFA.
