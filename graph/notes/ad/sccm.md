---
title: SCCM
---

System Center Configuration Manager (SCCM) aka Microsoft Endpoint Configuration Manager (MECM) is Microsoft's [[notes/network/software-deployment]] solution.

![SCCM site hierarchy ([source](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*kGVrrAJ2x1xLd2XgxTv6Ug.png))](./sccm-hierarchy.webp)

Discover SCCM servers over the network without authentication.

=== "builtin"
    ~~~ bat
    nslookup.exe type=SRV _mssms_mp_%sitecode%._tcp.corp.local
    ~~~

=== "[[notes/tools/nmap]]"
    Look for `commanName=SMS` in the script results ([source](https://twitter.com/naksyn/status/1628780091516788736)).

    ~~~ bash
    sudo nmap -vv -n -Pn -T4 --min-rate 1000 -sS -p 80,443,8530,8531,10123 -sV --version-intensity 0 --open
    ~~~

=== "[[notes/tools/httpx]]"
    ~~~ bash
    httpx -title -server -status-code -l ./computers.txt -path /ccm_system_windowsauth/request
    ~~~

Discover SCCM servers via LDAP.

=== "[[notes/tools/sccmhunter]]"
    ~~~ bash
    sccmhunter find -d corp.local -u jdoe -p 'passw0rd'
    sccmhunter smb -d corp.local -u jdoe -p 'passw0rd'
    sccmhunter show -users
    sccmhunter show -computers
    sccmhunter show -smb
    ~~~

=== "powershell"
    ~~~ powershell
    ([ADSISeacher]('objectClass=mSSMSManagementPoint')).FindAll() | %{$_.Properties}
    ~~~

Get site info on SCCM-managed computer.

=== "powershell"
    ~~~
    PS > Get-WMIObject -Namespace root\ccm -ClassName SMS_Authority
    ...
    CurrentManagementPoint : sccmmp01.corp.local
    Name                   : SMS:CRP
    ...
    ~~~

=== "[[notes/tools/sharpsccm]]"
    ~~~
    PS > .\SharpSCCM.exe local site-info
    ...
    Name: SMS:CRP
    ...
    ~~~

References:

- [Offensive SCCM Summary](http://web.archive.org/web/20240213175832/https://http418infosec.com/offensive-sccm-summary)
- [SCCM Exploitation: The First Cred Is the Deepest II - Gabriel Prud'homme](https://www.youtube.com/watch?v=W9PC9erm_pI), [slides](sccm-exploitation-the-first-is-the-deepest-part-2.pdf)
- [Microsoft Configuration Manager - New attack paths using ConfigMgr WebService extension](http://web.archive.org/web/20231013174032/https://www.shelltrail.com/research/microsoft-endpoint-configuration-manager-webservices/), abuse of WebService extension, keep an eye out for `OSDFrontEnd.exe.config`
- [The Hacker Recipes - SCCM/MECM](https://www.thehacker.recipes/a-d/movement/sccm-mecm)
- [SharpSCCM Demos - Black Hat 2023](https://www.youtube.com/watch?v=uyI5rgR0D-s)
- [SCCM Defensive Recommendations](https://github.com/Mayyhem/SharpSCCM/wiki#defensive-recommendations)
- [Active Directory Spotlight: Attacking The Microsoft Configuration Manager](http://web.archive.org/web/20230519210110/https://www.securesystems.de/blog/active-directory-spotlight-attacking-the-microsoft-configuration-manager/)
