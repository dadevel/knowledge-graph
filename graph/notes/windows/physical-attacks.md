---
title: Physical Attacks
---

Attacks against [[notes/windows/index]] computers that require physical access.

=== "builtin"
    Open `msinfo32.exe` window and check following values:

    - `Secure boot state` enabled for verified boot
    - `Kernel DMA protection` enabled to protect against [PCILeech](https://github.com/ufrisk/pcileech)
    - `Virtualisation-based security` enabled
    - `Device encryption support` enabled for full disk encryption

    Check BitLocker.

    ~~~ ps1
    Get-BitLockerVolume -MountPoint $env:SYSTEMDRIVE
    ~~~

=== "[ClientChecker.ps1](https://github.com/luemmelsec/client-checker)"
    ~~~ ps1
    irm 'https://github.com/LuemmelSec/Client-Checker/raw/main/Client-Checker.ps1' | iex
    Client-Checker
    ~~~

=== "[[notes/tools/netexec]]"
    ~~~ bash
    netexec smb ws01.corp.local -d corp.local -u jdoeadm -p 'passw0rd' -M wcc
    ~~~

Also check:

- BIOS password set?
- full disk encryption protected by TPM+PIN?

Untested tools:

- [MemProcFS](https://github.com/ufrisk/MemProcFS), supports PCILeech

References:

- [CVE-2022-41099 - Analysis of a BitLocker Drive Encryption Bypass](http://web.archive.org/web/20230814210937/https://blog.scrt.ch/2023/08/14/cve-2022-41099-analysis-of-a-bitlocker-drive-encryption-bypass/)
- [From BitLocker-Suspended to Virtual Machine](http://web.archive.org/web/20230421151812/https://sensepost.com/blog/2023/from-bitlocker-suspended-to-virtual-machine/), how to exploit "suspended" BitLocker with physical access
- [BIOS password recovery for laptops](https://bios-pw.org/)
