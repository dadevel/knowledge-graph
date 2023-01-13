---
title: WebDAV File Transfer
---

[[notes/file-transfer/index]] over the [[notes/network/webdav]] protocol.

# Client

WebDAV connections on Windows are handled by the *WebClient* service.
It is preinstalled on desktops, but not on servers.

Starting the service explicitly requires local admin rights, but it starts automatically when a WebDAV share is accessed over the GUI.
For example the command `start \\1.1.1.1@80\` can be used to trigger the service.
The command itself will fail, but that's intentional, so no Explorer window pops up.

Generally all Windows programs that expect absolute file paths also accept paths to network shares aka [UNC paths](https://learn.microsoft.com/en-us/dotnet/standard/io/file-path-formats#unc-paths).
See [[notes/file-transfer/smb]] for examples.

WebDAV path syntax:

~~~
# over http
\\192.0.2.1@8080\share\malware.exe
file://192.0.2.1@8080/share/malware.exe
# over https
\\192.0.2.1@ssl\share\malware.exe
\\192.0.2.1@ssl@8443\share\malware.exe
file://192.0.2.1@ssl/share/malware.exe
file://192.0.2.1@ssl@8443/share/malware.exe
# smb with fallback to webdav
\\192.0.2.1\share\malware.exe
~~~

# Server

With [[notes/tools/rclone]] over HTTP.

~~~ bash
rclone serve -v webdav . --addr :8080 --read-only
~~~

Alternatively over self-signed HTTPS.

~~~ bash
openssl req -newkey rsa:2048 -nodes -x509 -days 365 -keyout ./webdav.key -out ./webdav.crt
rclone serve -v webdav . --read-only --addr :8443 --cert ./webdav.crt --key ./webdav.key
~~~

Python [[notes/tools/wsgidav]] over HTTP ([source](https://twitter.com/Mr_0rng/status/1601408994932760576)).

~~~ bash
wsgidav --host 0.0.0.0 --port 8080 --auth anonymous --root .
~~~

Other tools:

- [goshs](https://github.com/patrickhener/goshs), simple HTTP and WebDAV server in Go
- The Nginx WebDAV module is to bare bones and does not work with Windows.
