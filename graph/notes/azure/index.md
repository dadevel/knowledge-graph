---
title: Azure
---

Microsofts cloud offering can be split into three main parts: The cloud provider Azure, the productivity suite [[notes/m365/index]] and the identity provider [[notes/entra/index]].

Azure Resource Manager (ARM) at [management.azure.com](https://management.azure.com) provides a central API for Azure and performs authorization based on role assignments (Azure RBAC).

Management scopes:

~~~
tenant
  root management group
    nested management groups
      subscriptions
        resource groups
          resources
~~~

Every subscription is assigned to exactly one tenant, but one tenant can have multiple subscriptions.

Overview of the default RBAC roles:

Role                      | Permissions
--------------------------|------------
Owner                     | full access to resources, manage access for other users
User Access Administrator | view resources, manage access for other users
Contributor               | full access to resources
Reader                    | view resources

Principals:

- Entra user
- Entra group
- Entra service principal
- user-assigned managed identity
- system-assigned managed identity

Role assignment: *principal* has *role* on *scope*.

For more info about individual resources check [[notes/azure/escalation]].

References:

- [XMGoat](https://github.com/XMCyber/XMGoat), setup vulnerable Azure environments and attack
- [Microsoft 365 Developer Program](https://developer.microsoft.com/en-us/microsoft-365/dev-program), free tenant including Office and Teams
