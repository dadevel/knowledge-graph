---
title: Intune
---

Intune is the software deployment and mobile device management solution for [[notes/m365/index]].

A user with *Global Administrator* or *Intune Administrator* role can execute blind PowerShell scripts in system context on all enrolled devices (likely including admin workstations).
Open [intune.microsoft.com](https://intune.microsoft.com), click `Devices/Scripts/Add/Windows 10 and later` and follow the wizard.
Set *Run this script using the logged on credentials* and *Enforce script signature check* to *no*, then assign the script to your target users or computers.
It can take multiple hours for the script to execute.

References:

- [Attacking Azure & Azure AD, Part II - Moving from Cloud to On-Premise](http://web.archive.org/web/20231028213625/https://scribe.rip/@specterops/attacking-azure-azure-ad-part-ii-5f336f36697d)
- [Death from above: Lateral movement from Azure to on-prem AD](http://web.archive.org/web/20221214191423/https://scribe.rip/@specterops/death-from-above-lateral-movement-from-azure-to-on-prem-ad-d18cb3959d4d)
