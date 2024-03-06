---
title: TCP File Transfer
---

[[notes/file-transfer/index]] over raw [[notes/network/tcp]] connections.

# Download

Sender, PowerShell [[notes/tools/powercat]].

~~~ powershell
powercat -l -p 8080 -i ./input.txt
~~~

Sender, Linux utilities.

~~~ bash
nc -lnvp 8080 -q 1 -w 1 < ./input.txt
socat -d -d tcp-listen:8080,reuseaddr,fork file:input.txt
~~~

Receiver, PowerShell [[notes/tools/powercat]].

~~~ powershell
powercat -c 192.0.2.1 -p 8080 -of ./output.txt
~~~

Receiver, Linux utilities.

~~~ bash
nc -v -q 1 -w 1 192.0.2.1 8080 > ./output.txt
socat -dd tcp:192.0.2.1:8080 file:output.txt,create
bash -c 'cat < /dev/tcp/192.0.2.1/8080 > ./output.txt'
~~~

# Upload

Receiver, PowerShell [[notes/tools/powercat]].

~~~ powershell
powercat -l -p 8080 -of ./output.txt
~~~

Receiver, Linux utilities.

~~~ bash
nc -lnvp 8080 -q 1 -w 1 > ./output.txt
socat -dd tcp-listen:8080,reuseaddr,fork file:output.txt,create
~~~

Sender, PowerShell [[notes/tools/powercat]].

~~~ powershell
powercat -c 192.0.2.1 -p 8080 -i ./input.txt
~~~

Sender, Linux utilities.

~~~ bash
nc -v -q 1 -w 1 192.0.2.1 8080 < ./input.txt
socat -d -d tcp:192.0.2.1:8080 file:input.txt
bash -c 'cat ./input.txt > /dev/tcp/192.0.2.1/8080'
~~~

Untested tools:

- [croc](https://github.com/schollz/croc)
