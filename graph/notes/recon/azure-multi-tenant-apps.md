---
title: Azure Multi-Tenant Apps
---

If a web app is configured as multi-tenant app instead of single-tenant, everybody with a Microsoft account can login and use the app while [[notes/entra/conditional-access]] rules apply only to users from the home tenant.

To check whether an app is multi-tenant, take the `client_id` URL parameter from the login page you were redirected to and try to retrieve info about the app.
This is only possible if multi-tenant authentication is enabled ([source](https://twitter.com/shirtamari/status/1643300698044391466)).

~~~ bash
az ad sp show --id $client_id
~~~

From an internal perspective query the database of [[notes/tools/roadtools]].

~~~ sql
SELECT displayName, availableToOtherTenants, appId, replyUrls FROM Applications WHERE availableToOtherTenants='1';
~~~

References:

- [BingBang: AAD misconfiguration led to Bing.com results manipulation and account takeover](http://web.archive.org/web/20230405062122/https://www.wiz.io/blog/azure-active-directory-bing-misconfiguration)
- [Azure AD multi-tenant app vs single tenant app](http://web.archive.org/web/20230403121747/https://merill.net/2023/04/azure-ad-multi-tenant-app-vs-single-tenant-app/)
