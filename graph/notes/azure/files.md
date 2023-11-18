---
title: Files
---

[[notes/azure/index]] Files publishes [[notes/azure/blob-storage]] as SMB share and supports Kerberos authentication.

Kerberos flow in Azure:

- Azure KDC proxy at `kerberos.microsoftonline.com`
- get TGT by posting to `login.microsoftonline.com/$tenantid/oauth2/token` with `tgt=true`
- get ST by posting the TGT to `login.microsoftonline.com/$tenantid/kerberos`
- pass the ST to Azure Files

Bounce the Ticket:

- dump TGT for Azure AD like any other TGT from a Windows computer
- pass the ticket to Azure Files
- potential path from on-prem to Azure

Silver Iodide:

- Kerberoasting STs for Azure Files is not viable, because the key is random
- when you control the Storage Account used by Azure Files you can get the key and impersonate any user against Azure Files

References:

- [Bounce the Ticket and Silver Iodide attacks on Azure AD Kerberos](http://web.archive.org/web/20230126000748/https://www.silverfort.com/wp-content/uploads/2023/01/Bounece-the-Ticket-and-Silver-Iodide-Attacks-on-Azure-AD-Kerberos-1.pdf)
