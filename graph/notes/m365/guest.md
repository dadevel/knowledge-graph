---
title: Guest Access
---

Guests can get some info from the tenant they're invited into.

=== "[[notes/tools/aadinternals]]"
    ~~~ powershell
    Get-AADIntAccessTokenForAzureCoreManagement -Tenant $tenantid
    $results = Invoke-AADIntReconAsGuest
    $results | gm
    $results.domains | Select-Object id,authen*,isverified,supported*,password* | Format-Table
    $results.allowedActions
    ~~~

Guests can not list users and groups, but they can list groups where a specific UPN (e.g. themself) is member and all members of this groups.
This means a guest can enumerate most users and groups in a tenant.

=== "[[notes/tools/aadinternals]]"
    ~~~ powershell
    Get-AADIntAccessTokenForAzureCoreManagement -Tenant $tenantid
    $results = Invoke-AADIntUserEnumerationAsGuest -GroupMembers -Manager -Subordinates -Roles
    $results.Groups | Select-Object displayName,id,membershiprule,description
    $results = Invoke-AADIntUserEnumerationAsGuest -UserName 'john.doe@corp.com' -GroupMembers -Manager -Subordinates -Roles
    ~~~

Guests can perform internal phishing via email or Teams.

Guests can access [[notes/m365/power-platform|Power Apps]] that are shared organization-wide.

References:

- [Quest for guest access: Azure Active Directory reconnaissance as a guest](http://web.archive.org/web/20231006135318/https://aadinternals.com/post/quest_for_guest/)
- [All You Need Is Guest](http://web.archive.org/web/20231026183239/https://i.blackhat.com/BH-US-23/Presentations/US-23-Bargury-All-You-Need-Is-Guest.pdf)
