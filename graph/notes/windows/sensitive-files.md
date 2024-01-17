---
title: Sensitive Files
---

[[notes/windows/index]] [[notes/mitre-attack/credential-access]]

Search for passwords in the PowerShell history and transcript logs.

=== "PowerShell"
    ~~~ powershell
    $patterns = 'passw|securestring|pscredential|net user |net use |connect-azaccount|save-azcontext'
    Get-ChildItem -ErrorAction SilentlyContinue -Force C:\Users\*\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\*.txt | Select-String -Pattern $patterns
    Get-ChildItem -ErrorAction SilentlyContinue -Force C:\Transcripts\*\*.txt | Select-String -Pattern $patterns
    ~~~

Recursively search for passwords in the current directory.

=== "PowerShell"
    ~~~ powershell
    Get-ChildItem -ErrorAction SilentlyContinue -Force -Recurse | Select-String -Pattern 'passw'
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
