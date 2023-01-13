---
title: SSH File Transfer
---

[[notes/file-transfer/index]] over the [[notes/network/ssh]] protocol.

# Client

Upload and download files with common Linux utilities.

~~~ bash
scp ./local.txt sshuser@192.0.2.1:remote.txt
scp sshuser@192.0.2.1:remote.txt ./local.txt 
scp -r ./local/ sshuser@192.0.2.1:remote/
scp -r sshuser@192.0.2.1:remote/ ./local/
rsync -r ./local/ sshuser@192.0.2.1:remote/
rsync -r sshuser@192.0.2.1:remote/ ./local/
~~~

`scp.exe` is preinstalled since Windows 10.
