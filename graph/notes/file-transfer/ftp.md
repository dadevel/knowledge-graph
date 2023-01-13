---
title: FTP File Transfer
---

[[notes/file-transfer/index]] over the [[notes/network/ftp]] protocol.

# Client

Download files with common Linux utilities.

~~~ bash
wget -O ./local.txt ftp://ftpuser:passw0rd@192.0.2.1:2121/remote.txt
curl -o ./local.txt -u ftpuser:passw0rd ftp://192.0.2.1:2121/remote.txt
curl -o ./local.txt ftp://ftpuser:passw0rd@192.0.2.1:2121/remote.txt
~~~

Upload and download files on Linux with the FTP client from `inetutils`.

~~~
❯ ftp -p 192.0.2.1
Name (192.0.2.1:owner): anonymous
Password: anonymous
ftp> get ./remote.txt
ftp> put ./local.txt
~~~

Download files with the builtin FTP client on Windows (causes firewall popup on first use, non-interactive authentication seems impossible).

~~~ bat
echo open 192.0.2.1 2121 > ftp.txt
echo USER anonymous >> ftp.txt
echo binary >> ftp.txt
echo get malware.exe >> ftp.txt
echo bye >> ftp.txt
ftp -v -n -s:ftp.txt
del ftp.txt
~~~

# Server

Start a read only FTP server with anonymous access.

~~~ bash
pip3 install --user pyftpdlib
python3 -m pyftpdlib -p 2121 -d ./srv
~~~

Or with authentication and write access.

~~~ bash
python3 -m pyftpdlib -p 2121 -u ftpuser -P 'passw0rd' -d ./srv -w
~~~
