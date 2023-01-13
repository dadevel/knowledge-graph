---
title: Shadow Copy
---

[[notes/windows/index]] Volume Shadow Copies.

Start the *Volume Shadow Copy* service if it is not already running.

~~~ bat
sc.exe start vss
~~~

List existing shadow copies.

=== "wmic"
    ~~~ bat
    wmic.exe shadowcopy list brief
    ~~~

=== "vssadmin"
    ~~~ bat
    vssadmin.exe list shadows
    ~~~

Create a new shadow copy.

=== "wmic"
    ~~~ bat
    wmic.exe shadowcopy call create volume=c:\
    ~~~

=== "vssadmin"
    ~~~ bat
    vssadmin.exe create shadow /for=c:
    ~~~

Delete a shadow copy.

=== "wmic"
    ~~~ bat
    wmic.exe shadowcopy delete /interactive
    ~~~

=== "vssadmin"
    ~~~ bat
    vssadmin.exe delete shadows /shadow={xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx}
    ~~~
