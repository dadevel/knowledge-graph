---
title: Version Detection
---

Microsoft software lifecycle:

1. Mainstream Support
    - free bug fixes
    - free feature updates
    - free security updates
    - free basic support depending on license
2. Extended Support
    - no bug fixes
    - no feature updates
    - free security updates
    - paid support
3. Extended Security Updates
    - no bug fixes
    - no feature updates
    - paid security updates
    - paid support

[[notes/windows/index]] build numbers:

Version      | Name
-------------|-----
Windows 5.0  | Windows 2000
Windows 5.1  | Windows XP
Windows 5.2  | Windows Server 2003 / 2003 R2
Windows 6.0  | Windows Vista / Windows Server 2008
Windows 6.1  | Windows 7 / Windows Server 2008 R2
Windows 6.2  | Windows 8 / Windows Server 2012
Windows 6.3  | Windows 8.1 / Windows Server 2012 R2
Windows 10.0 | Windows 10 / 11 / Windows Server 2016 / 2019 / 2022

> **Note:**
> Windows 10 2004, 20H2, 21H1, and 21H2 report the wrong build number `10.0.19041` over SMB ([source](http://web.archive.org/web/20230726144646/https://www.runzero.com/blog/fingerprinting-windows-smb/)).
> To get the correct version use the WMI query `SELECT Name, BuildNumber FROM Win32_OperatingSystem`.

References:

- [ESU Availability and End Dates](https://learn.microsoft.com/en-us/lifecycle/faq/extended-security-updates#esu-availability-and-end-dates)
