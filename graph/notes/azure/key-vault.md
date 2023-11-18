---
title: Key Vault
---

[[notes/azure/index]] Key Vaults are intended to store secrets like passwords, connection strings, certificates and private keys.
Azure resources that support managed identities like VMs or App Services can retrieve secrets from Key Vault.
The URL format is `https://VAULTNAME.vault.azure.net/(keys|secrets|certificates)/OBJECTNAME/OBJECTVERSION`.

Authorization on the management plane is handled exclusively with Azure RBAC.
The data plane supports additional Key Vault Access Policies.
If you have a role like Owner that can access the management plane you can modify the access policies to gain access to the secrets.

Built-in Role                               | Description                                                           | Secrets Access
--------------------------------------------|-----------------------------------------------------------------------|---------------
Key Vault Contributor                       | can manage key vaults                                                 | no
Key Vault Administrator                     | perform all data plane operations, cannot manage role assignment      | yes
Key Vault Certificates Officer              | perform any action on certificates, cannot manage permissions         | yes for certificates
Key Vault Crypto Officer                    | perform any action on keys, cannot manage permissions                 | yes for keys
Key Vault Secrets Officer                   | perform any action on secrets, cannot manage permissions              | yes for secrets
Key Vault Secrets User                      | read secret contents                                                  | yes for secrets
Key Vault Crypto Service Encryption User    | read metadata and perform wrap/unwrap operations on keys              | no
Key Vault Crypto User                       | perform cryptographic operations using keys                           | no
Key Vault Reader                            | read metadata of key vaults and its certificates, keys, and secrets   | no

Get an access token for Key Vault as application.

~~~ bash
roadtx auth -c f072c4a6-b440-40de-983f-a7f3bd317d8f -p 'passw0rd' -t defcorphq.onmicrosoft.com -r 'https://vault.azure.net' --as-app
~~~

Use code execution in context of a managed identity to get an access token for key vault.

~~~ bash
curl -sSf "$IDENTITY_ENDPOINT" -H "X-IDENTITY-HEADER: $IDENTITY_HEADER" -G -d api-version=2019-08-01 -d resource=https://vault.azure.net
~~~

Enumerate permissions on a key vault.

~~~ bash
curl -sSf "https://management.azure.com/subscriptions/$subscription_id/resourceGroups/Research/providers/Microsoft.KeyVault/vaults/ResearchKeyVault/providers/Microsoft.Authorization/permissions?api-version=2018-07-01" -H "Authorization: Bearer $access_token" | jq -r '.value[]'
~~~

Enumerate vault objects names.

~~~ bash
curl -sSf 'https://researchkeyvault.vault.azure.net/certificates?api-version=7.0' -H "Authorization: Bearer $vault_token" | jq -r '.value[].id'
curl -sSf 'https://researchkeyvault.vault.azure.net/keys?api-version=7.0' -H "Authorization: Bearer $vault_token" | jq -r '.value[].id'
curl -sSf 'https://researchkeyvault.vault.azure.net/secrets?api-version=7.0' -H "Authorization: Bearer $vault_token" | jq -r '.value[].id'
~~~

Retrieve secrets from vault object.

~~~ bash
curl -sSf "https://researchkeyvault.vault.azure.net/secrets/$object_name?api-version=7.0" -H "Authorization: Bearer $vault_token" | jq
~~~
