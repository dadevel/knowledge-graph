---
title: Registry
---

The [[notes/windows/index]] registry is used to store all kind of config options.

Read key and subkeys.

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-reg -k -no-pass srv01.corp.com query -keyName 'HKLM\System\CurrentControlSet\Control\Lsa' -s
    impacket-reg -k -no-pass srv01.corp.com query -keyName 'HKLM\System\CurrentControlSet\Control\Terminal Server' -s
    ~~~

=== "builtin"
    ~~~ bat
    reg.exe query "\\srv01.corp.com\HKLM\System\CurrentControlSet\Control\Lsa" /s
    reg.exe query "\\srv01.corp.com\HKLM\System\CurrentControlSet\Control\Terminal Server" /s
    ~~~

Read value.

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-reg -k -no-pass srv01.corp.com query -keyName 'HKLM\System\CurrentControlSet\Control\Lsa' -v DisableRestrictedAdmin
    impacket-reg -k -no-pass srv01.corp.com query -keyName 'HKLM\System\CurrentControlSet\Control\Terminal Server' -v fDenyTSConnections
    ~~~

=== "PowerShell"
    ~~~ powershell
    Get-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Lsa' -Name DisableRestrictedAdmin
    Get-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server' -Name fDenyTSConnections
    ~~~

=== "builtin"
    ~~~ bat
    reg.exe query "\\srv01.corp.com\HKLM\System\CurrentControlSet\Control\Lsa" /v DisableRestrictedAdmin
    reg.exe query "\\srv01.corp.com\HKLM\System\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections
    ~~~

Write value.

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-reg -k -no-pass srv01.corp.com add -keyName 'HKLM\System\CurrentControlSet\Control\Lsa' -v DisableRestrictedAdmin -vt REG_DWORD -vd 0
    impacket-reg -k -no-pass srv01.corp.com add -keyName 'HKLM\System\CurrentControlSet\Control\Terminal Server' -v fDenyTSConnections -vt REG_DWORD -vd 0
    ~~~

=== "PowerShell"
    ~~~ powershell
    New-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\LSA' -Name DisableRestrictedAdmin -PropertyType REG_DWORD -Value 0
    New-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server' -Name fDenyTSConnections -PropertyType REG_DWORD -Value 0
    ~~~

=== "builtin"
    ~~~ bat
    reg.exe add "\\srv01.corp.com\HKLM\System\CurrentControlSet\Control\Lsa" /v DisableRestrictedAdmin /t REG_DWORD /d 0 /f
    reg.exe add "\\srv01.corp.com\HKLM\System\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f
    ~~~

Delete value.

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-reg -k -no-pass srv01.corp.com delete -keyName 'HKLM\System\CurrentControlSet\Control\Lsa' -v DisableRestrictedAdmin
    impacket-reg -k -no-pass srv01.corp.com delete -keyName 'HKLM\System\CurrentControlSet\Control\Terminal Server' -v fDenyTSConnections
    ~~~

=== "PowerShell"
    ~~~ powershell
    Remove-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\LSA' -Name DisableRestrictedAdmin
    Remove-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server' -Name fDenyTSConnections
    ~~~

=== "builtin"
    ~~~ bat
    reg.exe delete /f "\\srv01.corp.com\HKLM\System\CurrentControlSet\Control\Lsa" /v DisableRestrictedAdmin
    reg.exe delete /f "\\srv01.corp.com\HKLM\System\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections
    ~~~

References:

- [The Defender’s Guide to the Windows Registry](http://web.archive.org/web/20230122191601/https://scribe.rip/@specterops/the-defenders-guide-to-the-windows-registry-febe241abc75)
