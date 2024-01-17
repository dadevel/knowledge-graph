---
title: ARM Templates
---

[[notes/azure/index]] ARM Templates provide an infrastructure as code service to deploy resources.
The templates are in JSON or Bicep format that contain the deployment configuration.

Azure keeps logs of the last 800 deployments.
Reading requires `Microsoft.Resources/deployments/read` and `Microsoft.Resources/subscriptions/resourceGroups/read`.
If a deployment parameter uses *String* instead of *SecureString* the password can be retrieved in clear text.

Enumerate deployments.
Check the output for secrets.

~~~ bash
curl -sSf "https://management.azure.com/subscriptions/$subscription_id/resourceGroups/$group_name/deployments?api-version=2020-01-01" -H "Authorization: Bearer $arm_token" | jq -r '.value[]'
~~~

Get the deployment template.
Check the output for secrets.

~~~ bash
curl -sSf "https://management.azure.com/subscriptions/$subscription_id/resourceGroups/$group_name/providers/Microsoft.Resources/deployments/BadExample_corp.onmicrosoft.com.stagingenv/exportTemplate?api-version=2021-04-01" -H "Authorization: Bearer $(jq -r .accessToken .roadtools_auth)" -d '' | jq
~~~

References:

- [Privilege Escalation from an ARM template](http://web.archive.org/web/20231203123133/https://scribe.rip/@rogierdijkman/project-miaow-9f334e8ec09e) and [miaow](https://github.com/SecureHats/miaow)
