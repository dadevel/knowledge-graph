---
title: Socat Tricks
---

[[notes/pivoting/index]] with [[notes/tools/socat]] by forwarding TCP connections, UDP connections and more.

# Port Redirection

Expose internal port `192.0.2.1:80` to the public.

~~~ bash
socat tcp-listen:8080,reuseaddr,fork tcp:192.0.2.1:80
~~~

Expose local Unix socket.

~~~ bash
socat tcp-listen:3307,reuseaddr,fork unix:/var/lib/mysql/mysql.sock
~~~

# Telnet

Poor mans telnet server.

~~~ bash
sudo socat tcp-listen:23,reuseaddr,fork exec:/bin/login,pty,setsid,setpgid,stderr,ctty
~~~

Poor mans telnet client.

~~~ bash
socat -,raw,echo=0 tcp:192.0.2.1:23
~~~

Telnet server with TLS client authentication.

~~~ bash
sudo socat openssl-listen:23,reuseaddr,fork,verify=1,cafile=./ca.pem,cert=./server.pem exec:/bin/bash,pty,setsid,setpgid,stderr,ctty
~~~

Telnet client with mutual TLS authentication.

~~~ bash
socat -,raw,echo=0 openssl:192.168.1.2:7023,verify=1,cafile=./ca.pem,cert./client.pem
~~~

# Miscellaneous

Open Unix socket.

~~~ bash
socat unix-listen:/tmp/socat.sock,fork -
~~~

Connect to TTY device (potential `minicom` replacement).

~~~ bash
socat readline /dev/ttyS0,raw,echo=0,crlf,sane
~~~

Share interactive program securly over the network.

~~~ bash
sudo socat -dd tcp-listen:5555,fork exec:/home/sandbox/app.sh,chroot=/home/sandbox,su=sandbox,pty,stderr
~~~

And connect to it.

~~~ bash
socat -,icanon=0,echo=0 tcp:localhost:5555
~~~
