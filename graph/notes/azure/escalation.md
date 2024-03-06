---
title: Azure Escalation
---

After compromise of a manged identity enumerate accessible [[notes/azure/index]] resources and abuse permissions to escalate further.

Enumerate subscriptions.

~~~ bash
curl -sSf 'https://management.azure.com/subscriptions?api-version=2021-04-01' -H "Authorization: Bearer $arm_token" | jq -r '.value[]'
~~~

Enumerate resource groups in subscription.

~~~ bash
curl -sSf "https://management.azure.com/subscriptions/$subscription_id/resourceGroups?api-version=2021-04-01" -H "Authorization: Bearer $arm_token" | jq -r '.value[]'
~~~

Enumerate resources in subscription.

~~~ bash
curl -sSf "https://management.azure.com/subscriptions/$subscription_id/resources?api-version=2021-04-01" -H "Authorization: Bearer $arm_token" | jq -r '.value[]'
~~~

Enumerate public IPs in a subscription.

~~~ bash
curl -sSf "https://management.azure.com/subscriptions/$subscription_id/providers/Microsoft.Network/publicIPAddresses?api-version=2023-05-01" -H 'Content-Type: application/json' -H "Authorization: Bearer $arm_token" | jq -r '.value[]|{name: .name, address: .properties.ipAddress}'
~~~

Exploitation of common resources:

- [[notes/azure/arm-templates]] and resource groups
- [[notes/azure/automation]]
- [[notes/azure/blob-storage]]
- [[notes/azure/function]]
- [[notes/azure/key-vault]]
- [[notes/azure/virtual-machine]]
- [[notes/azure/web-app]]

More interesting resources:

- content in Azure CosmosDB
- configuration of Azure Kubernetes Service
- Azure Batch Accounts and [extracting sensitive information from the Azure Batch Service](https://www.netspi.com/blog/technical/cloud-penetration-testing/extracting-sensitive-information-from-azure-batch-service/)
- Azure App Configuration Store

Untested tools:

- [AzDanglingDnsFinder](https://github.com/davidokeyode/AzDanglingDnsFinder), discovers subdomain takeover
- `Get-AzPasswords` in [MicroBurst](https://github.com/NetSPI/MicroBurst)
- [PowerZure](https://github.com/hausec/powerzure)

References:

- [Automating Managed Identity Token Extraction in Azure Container Registries](https://www.netspi.com/blog/technical/cloud-penetration-testing/automating-managed-identity-token-extraction-in-azure-container-registries/)
- [Azure built-in roles](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles), comprehensive list of Azure RBAC roles
- [IAM concepts](./azure-iam-concepts.pdf) from [Visualizing multi cloud IAM concepts](http://web.archive.org/web/20221212203821/https://scribe.rip/@julian-wieg/visualizing-multi-cloud-iam-concepts-63525967c0a7)
- [twitter.com/_wald0/status/1629007202509017089](https://twitter.com/_wald0/status/1629007202509017089), stealing managed identities from Azure Kubernetes Service (AKS)
- [Azure Policy Evaluator](https://azure.permissions.cloud/policyevaluator)
- [It’s raining shells - How to find new attack primitives in Azure by Andy Robbins](https://www.youtube.com/watch?v=a09_5SCPBZ0)
