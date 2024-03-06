---
title: Kernel Driver
---

Many 3rd-party [[notes/windows/index]] kernel drivers can be exploited to load rootkits or blind EDRs.
This is commonly known as *Bring your own vulnerable driver* (BYOVD), even so some drivers bring intended functionality that can be abused.

Notes:

- Microsoft maintains a blocklist of known vulnerable drivers, but the update process was broken for years
- the Defender ASR rule *Block abuse of exploited vulnerable signed drivers* appears to be useless ([source](http://web.archive.org/web/20221017071614/https://arstechnica.com/information-technology/2022/10/how-a-microsoft-blunder-opened-millions-of-pcs-to-potent-malware-attacks/))
- since Windows 11 vulnerable drivers are blocked by default, Windows 10 requires configuration with WDAC ([source](https://learn.microsoft.com/en-us/windows/security/threat-protection/windows-defender-application-control/microsoft-recommended-driver-block-rules))
- Hypervisor-Protected Code Integrity (HVCI) effectively prevents execution of unsigned code in the kernel space
- HVCI can be disabled by setting `HKLM\System\CurrentControlSet\Control\DeviceGuard\Scenarios\HypervisorEnforcedCodeIntegrity = 0`
- you might be able to bypass known vulnerable driver block lists by [[notes/windows/authenticode]] signature tampering

Untested tools:

- [IoctlHunter](https://github.com/z4ksec/ioctlhunter), analyses IOCTL calls
- [ioctlance](https://github.com/zeze-zeze/ioctlance), finds vulnerabilities in WDM drivers
- [hvci-loldrivers-check](https://github.com/trailofbits/HVCI-loldrivers-check), extracts HVCI blocklist on current system and compares against all drivers from [loldrivers.io](https://www.loldrivers.io/)
- [check_vulnerabledrivers.ps1](https://gist.github.com/api0cradle/d52832e36aaf86d443b3b9f58d20c01d), check installed drivers against [loldrivers.io](https://www.loldrivers.io/)
- [HackSysExtremeVulnerableDriver](https://github.com/hacksysteam/HackSysExtremeVulnerableDriver), driver to learn kernel exploitation, also see [Cracking HackSys Extreme Vulnerable Driver: where do I start?](http://web.archive.org/web/20240204095346/https://mdanilor.github.io/posts/hevd-0/)

References:

- [List of vulnerable drivers](https://github.com/eclypsium/Screwed-Drivers/blob/master/DRIVERS.md)
- [Living Off The Land Drivers](https://www.loldrivers.io/), authoritative reference
- [BYOVD Protection Is A Lie](http://web.archive.org/web/20231212011149/https://vu.ls/blog/byovd-protection-is-a-lie/)
- [Hunting Vulnerable Kernel Drivers](http://web.archive.org/web/20231101190125/https://blogs.vmware.com/security/2023/10/hunting-vulnerable-kernel-drivers.html) and [Driver Exploit PoCs](https://github.com/TakahiroHaruyama/VDR/tree/main/PoCs/firmware)
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
Get-WmiObject Win32_PnPSignedDriver | Select-Object DeviceName,DriverVersion,Manufacturer | ?{$_.Manufacturer -notlike 'Microsoft*' -and $_.Manufacturer -notlike 'Windows*' -and $_.Manufacturer -notlike '(Standard*'}
driverquery.exe /v /fo csv | ConvertFrom-CSV | Select-Object 'Display Name','Start Mode',Path
~~~
