---
title: Situational Awareness
---

Local [[notes/mitre-attack/discovery]] on [[notes/windows/index]] systems.

> **OpSec:** The examples below utilize common command line tools that will trigger detections in many organizations.

Untested tools:

- [User-Behavior-Mapping-Tool](https://github.com/trustedsec/User-Behavior-Mapping-Tool)

References:

- [Walking the Tightrope: Maximizing Information Gathering while Avoiding Detection for Red Teams](http://web.archive.org/web/20230518172300/https://www.trustedsec.com/blog/walking-the-tightrope-maximizing-information-gathering-while-avoiding-detection-for-red-teams/)
- [Oh, Behave! Figuring Out User Behavior](http://web.archive.org/web/20230131001306/https://www.trustedsec.com/blog/oh-behave-figuring-out-user-behavior/)

# User

Get groups and privileges of the current user.

~~~ bat
whoami.exe /all
~~~

Local users and groups.

~~~ bat
net.exe user
net.exe user administrator
net.exe localgroup
net.exe localgroup administrators
~~~

Local users and their SIDs.

=== "PowerShell"
    ~~~ powershell
    Get-CimInstance -ClassName Win32_UserAccount | Where-Object {$_.LocalAccount -eq $true} | ft -Property Name,SID
    Get-WmiObject -ClassName Win32_UserAccount | Where-Object {$_.LocalAccount -eq $true} | ft -Property Name,SID
    ~~~

=== "builtin"
    ~~~ bat
    wmic.exe useraccount get name,sid
    ~~~

User by SID.

=== "builtin"
    ~~~ bat
    wmic.exe useraccount where sid='S-1-5-21-...' get name,fullname
    ~~~

Sessions.

~~~ bat
query.exe session
query.exe user
~~~

Recent logons (requires privileged access).

=== "PowerShell"
    ~~~ powershell
    Get-EventLog Security -InstanceId 4624 -Newest 100
    ~~~

=== "builtin"
    ~~~ bat
    wevtutil.exe qe security /rd:true /c:100 /f:xml /q:"*[System[(EventID=4624)]]"
    ~~~

# System info

OS version and other info.

=== "PowerShell"
    ~~~ powershell
    Get-ComputerInfo | fl -Property CsUserName,LogonServer,CsDNSHostName,CsDomain,CsDomainRole,OsName,OsVersion,OsArchitecture,KeyboardLayout,CsHypervisorPresent,CsManufacturer,CsModel
    ~~~

=== "builtin"
    ~~~ bat
    hostname.exe
    ver
    systeminfo.exe
    ~~~

Installed endpoint protection.

=== "PowerShell"
    ~~~ powershell
    Get-CimInstance -Namespace root/SecurityCenter2 -ClassName AntivirusProduct | fl -Property DisplayName
    Get-WmiObject -Namespace root/SecurityCenter2 -ClassName AntivirusProduct | fl -Property DisplayName
    ~~~

=== "builtin"
    ~~~ bat
    wmic.exe /namespace:\\root\SecurityCenter2 path AntiVirusProduct get DisplayName
    ~~~

# Environment

All environment variables.

=== "PowerShell"
    ~~~ powershell
    ls env:
    ~~~

=== "builtin"
    ~~~ bat
    set
    ~~~

# Network

Interfaces and addresses.

=== "builtin"
    ~~~ bat
    ipconfig.exe /all
    ~~~

Routes.

=== "builtin"
    ~~~ bat
    route.exe print
    ~~~

ARP neighbors.

=== "builtin"
    ~~~ bat
    arp -a
    ~~~

Listening sockets.

=== "PowerShell"
    ~~~ powershell
    Get-NetTcpConnection -State Listen | Select-Object -Property *,@{'Name' = 'ProcessName';'Expression'={(Get-Process -Id $_.OwningProcess).Name}} | ft -Property LocalAddress,LocalPort,ProcessName
    ~~~

=== "bulitin"
    ~~~ bat
    netstat.exe -ano | findstr.exe /i listening
    ~~~

Outgoing connections.

=== "PowerShell"
    ~~~ powershell
    Get-NetTcpConnection -State Established | Select-Object -Property *,@{'Name' = 'ProcessName';'Expression'={(Get-Process -Id $_.OwningProcess).Name}} | ft -Property LocalAddress,LocalPort,ProcessName
    ~~~

Recent DNS lookups ([source](https://twitter.com/EricaZelic/status/1691911899850654190)).

=== "PowerShell"
    ~~~ powershell
    Get-DNSClientCache
    ~~~

=== "builtin"
    ~~~ bat
    ipconfig.exe /displaydns
    ~~~

Firewall rules.

=== "PowerShell"
    ~~~ powershell
    Get-NetFirewallRule -PolicyStore ActiveStore | Where-Object {$_.Enabled} | ft -Property DisplayName,Direction,Action
    Get-NetFirewallRule | ft -Auto -Property Name,@{Name='Protocol';Expression={($PSItem | Get-NetFirewallPortFilter).Protocol}},@{Name='LocalPort';Expression={($PSItem | Get-NetFirewallPortFilter).LocalPort}},@{Name='RemotePort';Expression={($PSItem | Get-NetFirewallPortFilter).RemotePort}},@{Name='RemoteAddress';Expression={($PSItem | Get-NetFirewallAddressFilter).RemoteAddress}},Enabled,Profile,Direction,Action
    ~~~

=== "builtin"
    ~~~ bat
    netsh.exe advfirewall show currentprofile
    netsh.exe advfirewall firewall show rule name=all dir=in
    netsh.exe advfirewall firewall show rule name=all dir=out
    ~~~

Programs that are allowed to initiate outbound connections.

~~~ powershell
Get-NetFirewallRule -PolicyStore ActiveStore | Where-Object {$_.Enabled -and $_.Direction -eq 'Outbound' -and $_.Action -eq 'Allow'} | Get-NetFirewallApplicationFilter | ft -Property Program,InstanceID
~~~

# Process info

Running processes.

=== "PowerShell"
    ~~~ powershell
    Get-CimInstance -ClassName Win32_Process | Where-Object {$_.Name -ne 'svchost.exe'} | ft -Property Name,ProcessId,Path,CommandLine
    Get-WmiObject -ClassName Win32_Process | Where-Object {$_.Name -ne 'svchost.exe'} | ft -Property Name,ProcessId,Path,CommandLine
    Get-Process | Where-Object {$_.Name -ne 'svchost'} | ft -Property Name,Id,Path
    ~~~

=== "builtin"
    ~~~ bat
    tasklist.exe
    tasklist.exe /v
    ~~~

Processes and associated services.

=== "builtin"
    ~~~ bat
    tasklist.exe /svc
    ~~~

Processes executed by current user (filtering by other users requires elevated privileges).

~~~ bat
tasklist.exe /v /fi "username eq %USERDOMAIN%\%USERNAME%"
~~~

Processes that loaded a specific DLL.

~~~ bat
tasklist.exe /m:ntdll.dll
~~~

# Services and Scheduled Tasks

3rd-party services.

=== "PowerShell"
    ~~~ powershell
    Get-CimInstance -ClassName Win32_Service | Where-Object {$_.PathName -notlike 'C:\Windows\System32\*'} | ft -Property Name,State,StartMode,StartName,PathName
    Get-WmiObject -ClassName Win32_Service | Where-Object {$_.PathName -notlike 'C:\Windows\System32\*'} | ft -Property Name,State,StartMode,StartName,PathName
    Get-Service | ft -Property Name,Status,StartType
    ~~~

=== "builtin"
    ~~~ bat
    wmic.exe service get name,pathname,state,startmode | findstr /i /v c:\windows\system32
    sc.exe query type= service state= all
    sc.exe queryex type= service state= all
    services.msc
    ~~~

3rd-party scheduled tasks.

=== "PowerShell"
    ~~~ powershell
    Get-ScheduledTask | Where-Object {$_.State -ne 'disabled' -and $_.Author -notlike 'Microsoft*'} | Select-Object -Property '*' -ExpandProperty Actions -ExcludeProperty PSComputerName,CimClass,CimInstanceProperties,CimSystemProperties | ft -Property TaskName,Execute,Arguments,ClassId,Data
    ~~~

=== "builtin"
    ~~~ bat
    schtasks.exe /query /fo list /v
    ~~~

# Applications

Installed 3rd-party software.

=== "PowerShell"
    ~~~ powershell
    Get-CimInstance -ClassName Win32_Product | Where-Object {$_.Vendor -notmatch 'Microsoft*'} | ft -Property Vendor,Name,Version
    Get-WmiObject -ClassName Win32_Product | Where-Object {$_.Vendor -notmatch 'Microsoft*'} | ft -Property Vendor,Name,Version
    ~~~

=== "builtin"
    ~~~ bat
    wmic.exe product get vendor,name,version
    ~~~

Installed 3rd-party software, low-tech version.

~~~ bat
dir "C:\Program Files"
dir "C:\Program Files (x86)\"
~~~

# Filesystem

Files in current dir.

=== "PowerShell"
    ~~~ powershell
    ls -force
    ~~~

=== "builtin"
    ~~~ bat
    dir /a /o:gn /q /r
    ~~~

Files recursive.

~~~ bat
dir /a /o:gn /q /r /s
~~~

PowerShell scripts.

~~~ powershell
Get-Childitem -ErrorAction SilentlyContinue –Force -Recurse -Path C:\ -File -Include *.ps1
~~~

Last written files.

~~~ powershell
Get-ChildItem -ErrorAction SilentlyContinue -Force -Recurse -Path C:\ -File | Sort-Object -Property LastWriteTime | ft -Property LastWriteTime,FullName
~~~

Files owned by current user.

~~~ powershell
Get-ChildItem -ErrorAction SilentlyContinue -Force -Recurse -Path .\Downloads\ -File | Get-ACL | Where-Object {$_.Owner -eq "$env:USERDOMAIN\$env:USERNAME"} | ft -Property PSPath
~~~

Drives.

~~~ bat
fsutil.exe fsinfo drives
mountvol.exe
~~~
