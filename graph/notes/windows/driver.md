---
title: Kernel Driver
---

Many 3rd-party [[notes/windows/index]] kernel drivers can be exploited to load root kits or blind EDRs.
This is commonly known as *Bring your own vulnerable driver* (BYOVD).

Untested tools:

- [check_vulnerabledrivers.ps1](https://gist.github.com/api0cradle/d52832e36aaf86d443b3b9f58d20c01d), check installed drivers against [loldrivers.io](https://www.loldrivers.io/)

References:

- [Living Off The Land Drivers](https://www.loldrivers.io/), authoritative reference
- [Journey into Windows Kernel Exploitation: The Basics](http://web.archive.org/web/20230820105350/https://scribe.rip/@neuvik/journey-into-windows-kernel-exploitation-the-basics-fff72116ca33)
- [gist.github.com/yardenshafir/048a957e7e52978b32e43a7e4e1e72bb](https://gist.github.com/yardenshafir/048a957e7e52978b32e43a7e4e1e72bb), vulnerable drivers from [loldrivers.io](https://www.loldrivers.io/) that load with HVCI blocklist version 25314
- [Backdoors for Cross-Signed Drivers](http://web.archive.org/web/20230721015754/https://www.geoffchappell.com/notes/security/whqlsettings/index.htm), setting `HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\CI\Policy\UpgradedSystem` to `1` allows loading of cross-signed drivers
- [Lord Of The Ring0 - Part 4 | The call back home](http://web.archive.org/web/20230306201837/https://idov31.github.io/2023/02/24/lord-of-the-ring0-p4.html)
- [TransitionalPeriod](https://github.com/RobinFassinaMoschiniForks/TransitionalPeriod), kernel to user mode shellcode exploits
- [A syscall journey in the Windows kernel](http://web.archive.org/web/20221126094327/https://alice.climent-pommeret.red/posts/a-syscall-journey-in-the-windows-kernel/)

List drivers.
Focus on 3rd-party drivers.
Drivers marked as `stopped` can still be interacted with.

~~~ powershell
Get-WmiObject Win32_PnPSignedDriver | Select-Object DeviceName,DriverVersion,Manufacturer
driverquery.exe /v /fo csv | ConvertFrom-CSV | Select-Object 'Display Name','Start Mode',Path
~~~
