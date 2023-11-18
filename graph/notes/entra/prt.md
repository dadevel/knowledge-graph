---
title: PRT
---

A Primary Refresh Token is issued only on Azure-joined or hybrid-joined devices.
During registration, a device key pair and a transport key pair are generated.
While the private keys are bound to the TPM of the device, the public keys are sent to AAD and the device receives a session key encrypted with the public transport key.
Therefore the session key can only be decrypted by the TPM.
All access token requests or PRT renewals are signed by the TPM with this session key ([source](https://learn.microsoft.com/en-us/azure/active-directory/devices/concept-primary-refresh-token)).

Once issued, a PRT is valid for 14 days and continuously renewed as long as the user actively uses the device.
[[notes/entra/conditional-access]] policies are not evaluated when PRTs are renewed ([source](https://learn.microsoft.com/en-us/azure/active-directory/devices/concept-primary-refresh-token)).

When a user initiates a browser interaction, a browser extension communicates with the `BrowserCore.exe` native messaging host.
This program requests a PRT cookie, which is signed with the TPM-protected session key.
This PRT-cookie is then included as `x-ms-RefreshTokenCredential` header to request a pair of access and refresh tokens from AAD.
The tokens issued by this process will have the same claims the PRT had.
So in most cases MFA and device compliance requirements are satisfied ([source](http://web.archive.org/web/20221226162133/https://dirkjanm.io/abusing-azure-ad-sso-with-the-primary-refresh-token/)).
This can be abused with [[notes/entra/pass-the-cookie]].
