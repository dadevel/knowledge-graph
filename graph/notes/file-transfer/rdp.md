---
title: RDP File Transfer
---

[[notes/file-transfer/index]] over the [[notes/network/rdp]] protocol.

Connect to an RDP server from Linux and make the local directory `./srv` accessible under `\\tsclient\share` on the server.

=== "[[notes/tools/freerdp]]"
    ~~~ bash
    mkdir ./srv
    xfreerdp /cert:ignore +clipboard /dynamic-resolution /tls-seclevel:0 /drive:share,./srv /v:srv01.corp.local /u:jdoeadm /p:'passw0rd'
    ~~~

Connect to an RDP server from Windows and map all local drives to the server.

=== "builtin"
    ~~~ bat
    echo full address:s:srv01.corp.local > .\example.rdp
    echo authentication level:i:0 >> .\example.rdp
    echo drivestoredirect:s:* >> .\example.rdp
    mstsc.exe .\example.rdp
    ~~~

![Map drives trough the GUI](./mstsc-drive-map.png)
