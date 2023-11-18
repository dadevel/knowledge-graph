---
title: Cloud Kerberos Trust
---

The on-prem AD trusts a virtual RODC in [[notes/entra/index]] named `AzureADKerberos`.
TGTs issued by Entra can be used to authenticate against on-prem resources.
This allows escalation from global admin to on-prem domain admin.

References:

- [(Windows) Hello from the other side](http://web.archive.org/web/20230706173016/https://dirkjanm.io/assets/raw/Windows%20Hello%20from%20the%20other%20side_TR23_final.pdf), [talk](https://www.youtube.com/watch?v=AFay_58QubY)
- [Obtaining Domain Admin from Azure AD by abusing Cloud Kerberos Trust](http://web.archive.org/web/20230625100743/https://dirkjanm.io/obtaining-domain-admin-from-azure-ad-via-cloud-kerberos-trust) with [roadtools-hybrid](https://github.com/dirkjanm/ROADtools_hybrid)
- [A Demonstrated Abuse of Cloud Kerberos Trust - Daniel Heinsen & Elad Shamir - fwd:cloudsec 2023](https://www.youtube.com/watch?v=tR06WBbqnL0), [slides](http://web.archive.org/web/20230625102219/https://eladshamir.com/uploads/fwdcloudsec2023/Slides.pdf)
