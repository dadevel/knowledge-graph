---
title: TFTP File Transfer
---

[[notes/file-transfer/index]] over the [[notes/network/tftp]] protocol.

# Client

Upload and download files with a Windows builtin (no longer preinstalled on Windows 10, but still available on latest Windows Server).

~~~ bat
tftp.exe -i 192.0.2.1 put .\local.txt
tftp.exe -i 192.0.2.1 get remote.txt .\local.txt
~~~

Upload and download files on Linux with `tftp-hpa`.

~~~
❯ tftp 192.0.2.1
tftp> put local.txt
tftp> get remote.txt
~~~

# Server

Start a TFTP server on Linux.

~~~ bash
mkdir ./srv
sudo chown -R nobody:nobody ./srv
sudo atftpd --daemon --no-fork --logfile /dev/stderr --user nobody --group nobody --port 69 ./srv
~~~
