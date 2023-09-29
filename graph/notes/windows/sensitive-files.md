---
title: Sensitive Files
---

[[notes/windows/index]] [[notes/mitre-attack/credential-access]]

Search for passwords in the PowerShell history.

=== "PowerShell"
    ~~~ powershell
    Get-ChildItem -ErrorAction SilentlyContinue -Force ~\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\*.txt | Select-String -Pattern 'passw|secure-string|save-azcontext' | Select-Object -Property Line
    ~~~

=== "builtin"
    ~~~ bat
    findstr.exe /i passw %userprofile%\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\*.txt
    ~~~

Recursively search for passwords in the current directory.

=== "PowerShell"
    ~~~ powershell
    Get-ChildItem -ErrorAction SilentlyContinue -Force -Recurse | Select-String -Pattern 'passw' | Format-Table -AutoSize -Property Path,Line
    ~~~

=== "builtin"
    ~~~ bat
    findstr.exe /si passw .\*
    ~~~

Other sensitive files:

~~~
~/.Azure/AzureRmContext.json
~/.Azure/TokenCache.dat
~~~

List files in recycle bin.

~~~ bat
dir C:\$Recycle.Bin
~~~

Decrypt a file encrypted as *PowerShell Secure String*.

~~~ powershell
$aeskey = Get-Content ./pkginstaller.key
$ciphertext = Get-Content ./pkginstaller.cred | ConvertTo-SecureString -Key $aeskey
$plaintext = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($ciphertext))
echo $plaintext
~~~
