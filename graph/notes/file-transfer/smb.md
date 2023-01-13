---
title: SMB File Transfer
---

[[notes/file-transfer/index]] over the [[notes/network/smb]] protocol.

# Client

Linux Samba.

~~~
❯ smbclient -U administrator%'passw0rd' //192.0.2.1/share
smb: \> put local.txt
smb: \> get remote.txt
~~~

Python [[notes/tools/impacket]] (can be unreliable with large files over spotty connections).

~~~
❯ impacket-smbclient administrator:'passw0rd'@192.0.2.1
# use share
# put local.txt
# get remote.txt
~~~

Generally all Windows programs that expect absolute file paths also accept paths to network shares aka [UNC paths](https://learn.microsoft.com/en-us/dotnet/standard/io/file-path-formats#unc-paths).

Copy files in PowerShell.

~~~ powershell
cp ./local.txt //192.0.2.1/share/
cp //192.0.2.1/share/remote.txt .
~~~

Copy directories in PowerShell.

~~~ powershell
cp . //192.0.2.1/share -Recurse
cp //192.0.2.1/share . -Recurse
~~~

Authenticate against a share in PowerShell.

~~~ powershell
New-PSDrive -PSProvider FileSystem -Persist -Name S -Root \\192.0.2.1\share -Credential (New-Object System.Management.Automation.PsCredential('smbuser', (ConvertTo-SecureString 'passw0rd' -AsPlainText -Force)))
~~~

Copy files with Windows builtins.

~~~ bat
copy /y .\local.txt \\192.0.2.1\share\remote.txt
copy /y \\192.0.2.1\share\remote.txt .\local.txt
~~~

Copy directories with Windows builtins.

~~~ bat
robocopy.exe /e . \\192.0.2.1\share
robocopy.exe /e \\192.0.2.1\share .
~~~

Authenticate against a share with Windows builtins.

~~~ bat
net.exe use \\192.0.2.1\share "passw0rd" /user:smbuser
net.exe use \\192.0.2.1\share /delete
~~~

# Server

Python [[notes/tools/impacket]].

~~~ bash
sudo impacket-smbserver -smb2support share ./srv  # anonymous access
sudo impacket-smbserver -smb2support -username smbuser -password 'passw0rd' share ./srv
~~~
