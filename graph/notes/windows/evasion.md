---
title: Windows Evasion
---

[[notes/mitre-attack/defense-evasion]] tricks for [[notes/windows/index]].

List installed endpoint protection solutions.

=== "builtin"
    ~~~ bat
    wmic.exe /node:localhost /namespace:\\root\SecurityCenter2 Path AntiVirusProduct Get DisplayName
    ~~~

Detect installed endpoint protections by enumerating known named pipes and services remotely as unprivileged user.

=== "[[notes/tools/servicedetector]]"
    ~~~ bash
    servicedetector -k -no-pass ws01.corp.local
    ~~~

=== "[[notes/tools/crackmapexec]]"
    ~~~ bash
    crackmapexec smb ws01.corp.local -u jdoe -p 'passw0rd' -M enum_av
    ~~~

    [source](https://twitter.com/mpgn_x64/status/1628720939532750849)

Find excluded processes by checking if they have the userland hooking DLL of the endpoint protection loaded with [CheckDLLs.ps1](https://gist.github.com/dadevel/e89e7089a2e01446caf22bbef6738e94).
An alternate tool for this is [Bin-Finder](https://github.com/Kudaes/Bin-Finder).

~~~ powershell
Import-Module ./CheckDLLs.ps1
Get-Process | Check-DLLs -ModuleNames 'InProcessClient.dll', 'InProcessClient64.dll', 'MinProcessClient.dll', 'MinProcessClient64.dll' | ?{!$_.'InProcessClient.dll' -and !$_.'InProcessClient64.dll'} | ft -auto
~~~

Untested tools:

- [TimeException](https://github.com/bananabr/TimeException), detect excluded folders trough timing discrepancies
- [Forensia](https://github.com/PaulNorman01/Forensia), purge various forensic artifacts

References:

- [Red Teaming in the EDR age - Wild West Hackin' Fest 2018](https://www.youtube.com/watch?v=l8nkXCOYQC4)
- [docs.google.com/spreadsheets/u/0/d/1ZMFrD6F6tvPtf_8McC-kWrNBBec_6Si3NW6AoWf3Kbg/htmlview](https://docs.google.com/spreadsheets/u/0/d/1ZMFrD6F6tvPtf_8McC-kWrNBBec_6Si3NW6AoWf3Kbg/htmlview), telemetry sources of common EDRs
- [twitter.com/Cyb3rMonk/status/1648743976407531525](https://twitter.com/Cyb3rMonk/status/1648743976407531525), EDRs cant log every event due to shear volume
- [Microsoft Anti-Virus exclusion recommendations by application](http://web.archive.org/web/20230101000458/https://social.technet.microsoft.com/wiki/contents/articles/953.microsoft-anti-virus-exclusion-list.aspx)

# Blinding EDRs

Stop the EDR from reporting to its cloud API as local admin ([source](https://twitter.com/Z3rO_C00L/status/1570837519453007872)).

~~~ bat
echo 0.0.0.0 api.vendor.com >> c:\windows\system32\drivers\etc\hosts
~~~

Alternatively you can block outgoing network connections for the EDR processes with the Windows firewall.

EDRs use [[notes/windows/ppl|PPL]] to prevent their processes from being stopped, but they still can be suspended ([source](http://web.archive.org/web/20230325071705/https://www.trustedsec.com/blog/disabling-av-with-process-suspension/)).
Most AVs and EDRs block this attack with their kernel callbacks.
For example with [pssuspend](https://learn.microsoft.com/en-us/sysinternals/downloads/pssuspend) from SysInternals or [sus.ps1](https://github.com/0xv1n/proc-suspend/blob/main/sus.ps1) ([source](https://twitter.com/0gtweet/status/1638069413717975046)).

~~~ bat
.\pssuspend.exe msmpeng.exe
~~~

Writing the following registry value causes the target process to crash shortly after startup ([source](https://web.archive.org/web/20230507150230/https://www.trendmicro.com/en_us/research/23/e/attack-on-security-titans-earth-longzhi-returns-with-new-tricks.html)).
This is blocked by most AVs and EDRs.

~~~
HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\MsMpEng.exe\MinimumStackCommitInBytes = 0x88888888
~~~

Disable EDR services trough registry export and reimport ([source](https://twitter.com/0gtweet/status/1684907177117454336)).
This works against some AVs and maybe even against some EDRs.

- open `regedit.exe` as administrator
- export `HKLM\SYSTEM\CurrentControlSet` to a `.save` file (not `.reg`)
- note executable names of EDR services and drivers
- edit the `.save` file with a hex editor (e.g. [HxD](https://mh-nexus.de/en/downloads.php?product=HxD20)) and replace a character in the executable path of all EDR services
- create the key `HKLM\SYSTEM\ControlSet002`
- import the `.save` file under that key
- set the following values under `HKLM\SYSTEM\Select`
    - `Current` = `2`
    - `Default` = `2`
    - `LastKnownGood` = `2`
- reboot

Untested tools:

- [KDU](https://github.com/hfiref0x/KDU), exploit various vulnerable drivers to hijack protected processes or load unsigned drivers
- [OffensivePH](https://github.com/RedSection/OffensivePH), uses old Process Hacker driver to inject shellcode into PPL processes
- [TokenUniverse](https://github.com/diversenok/TokenUniverse), GUI to tamper with Windows tokens and many other objects
- [NerfToken-Go](https://github.com/tnpitsecurity/nerftoken-go), modify process tokens of [[notes/windows/ppl|PPL]] processes to remove their privileges as system ([source](https://www.elastic.co/security-labs/sandboxing-antimalware-products)), patched in Windows 11 22H2 ([source](https://twitter.com/yarden_shafir/status/1628049645896183809))
- [Kernel-Cactus](https://github.com/spikysabra/kernel-cactus), didn't compile
- [RIPPL](https://github.com/last-byte/rippl/), uses technique from [PPLdump](https://github.com/itm4n/PPLdump) to tamper with protected processes, patched since Windows 10 21H2 Build 19044.1826 ([source](https://itm4n.github.io/the-end-of-ppldump/)), but EDR tamper methods like pausing instead of killing EDR processes are still interesting

References:

- [Old certificate, new signature: Open-source tools forge signature timestamps on Windows drivers](http://web.archive.org/web/20230712010119/https://blog.talosintelligence.com/old-certificate-new-signature/)
- [Attacking an EDR - Part 2](http://web.archive.org/web/20230914130817/https://her0ness.github.io/2023-09-14-Attacking-an-EDR-Part-2/), disable EDRs tamper protection by intercepting an API response with Burp
- [Reverse Engineering Windows Defender's Antivirus Emulator - Black Hat 2018](https://www.youtube.com/watch?v=wDNQ-8aWLO0)
- [Attacking an EDR - Part 1](http://web.archive.org/web/20230804174921/https://riccardoancarani.github.io/2023-08-03-attacking-an-edr-part-1/), EDR whitelisted own helper process, but did not protect it, detected because process didn't hat the EDRs hooking DLL loaded
- [Dissecting the Windows Defender Driver - WdFilter (Part 1)](http://web.archive.org/web/20230204015856/https://n4r1b.com/posts/2020/01/dissecting-the-windows-defender-driver-wdfilter-part-1/)
- [Attacking on Behalf of Defense: DLL Sideloading EDR Binaries](http://web.archive.org/web/20230627204035/https://mansk1es.gitbook.io/edr-binary-abuse/)
- [Operators, EDR Sensors, and OODA Loops](http://web.archive.org/web/20230802194355/https://jackson_t.gitlab.io/ooda-loops.html)
- [Bypass Protected Process Light using Process Explorer](http://web.archive.org/web/20230101000147/https://waawaa.github.io/en/Bypass-PPL-Using-Process-Explorer/)
- [Bypass PPL from user-mode using a vulnerable driver](https://www.unknowncheats.me/forum/anti-cheat-bypass/262766-bypass-ppl-protected-process-light-user-mode-using-vulnerable-driver.html)

# EDR Kernel Unhooking

Evade EDRs by loading a signed but dangerous dangerous driver to tamper with kernel callbacks.

Tested tools:

- [EDRSandblast-GodFault](https://github.com/gabriellandau/EDRSandblast-GodFault), removes kernel hooks without a kernel driver trough [GodFault](https://github.com/gabriellandau/PPLFault#godfault) ([source](http://web.archive.org/web/20230901211135/https://www.elastic.co/security-labs/forget-vulnerable-drivers-admin-is-all-you-need))
- [EDRSandblast](https://github.com/wavestone-cdt/edrsandblast/tree/defcon30release), uses `RTCore64.sys` or `DBUtils_2_3.sys`, pain to setup, but works well
- [CheekyBlinder](https://github.com/br-sn/cheekyblinder), less features then EDRSandblast

Untested tools:

- [EchoDrv](https://github.com/YOLOP0wn/EchoDrv), remove kernel hooks trough `echo_driver.sys`

References:

- [Silencing the EDR - How to disable process, threads and image-loading detection callbacks](http://web.archive.org/web/20221111123625/https://www.matteomalvica.com/blog/2020/07/15/silencing-the-edr/)
- [Driver-based attacks: Past and present](http://web.archive.org/web/20230101000144/https://www.rapid7.com/blog/post/2021/12/13/driver-based-attacks-past-and-present/)
- [Removing kernel callbacks using signed drivers](http://web.archive.org/web/20221002160329/https://br-sn.github.io/Removing-Kernel-Callbacks-Using-Signed-Drivers/)

# Killing EDRs

Tested tools:

- [Terminator](https://github.com/ZeroMemoryEx/Terminator), uses `zam64.sys` to kill processes
- [Backstab](https://github.com/yaxser/backstab), uses Process Explorer driver, worked only partially
- [Breakcyserver](https://github.com/waawaa/breakcyserver), uses Process Explorer driver, didn't work

Untested tools:

- [LOLDrivers Finder](https://github.com/xalicex/LOLDrivers_finder/blob/main/finder.py), search LolDrivers for drivers that can kill processes
- [mhydeath](https://github.com/zer0condition/mhydeath), uses `mhyprotect.sys`
- [NVDrv](https://github.com/zer0condition/NVDrv), uses `nvoclock.sys` to read arbitrary memory
- [Ryzen Master Exploit](https://github.com/tijme/amd-ryzen-master-driver-v17-exploit/), BOF for exploiting AMD's Ryzen Master Driver v17
- [Killers](https://github.com/xalicex/Killers), uses driver from Avast or IOBit Malware Fighter
- [Blackout](https://github.com/ZeroMemoryEx/Blackout), uses GMER driver

References:

- [ThreadSleeper: Suspending Threads via GMER64 Driver](http://web.archive.org/web/20230719203839/https://www.binarydefense.com/resources/blog/threadsleeper-suspending-threads-via-gmer64-driver/), don't kill EDR processes, instead suspend all its threads
- [twitter.com/malmoeb/status/1551449530729730049](https://twitter.com/malmoeb/status/1551449530729730049), thread about vulnerable Gigabyte `gdrv.sys` driver
- [twitter.com/wdormann/status/1663741856461598724](https://twitter.com/wdormann/status/1663741856461598724), thread about GMER driver and `truesight.sys`
