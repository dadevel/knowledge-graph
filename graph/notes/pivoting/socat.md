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
socat tcp-listen:23,reuseaddr,fork exec:/bin/login,pty,setsid,setpgid,stderr,ctty
~~~

Poor mans telnet client.

~~~ bash
socat stdio,raw,echo=0 tcp:192.0.2.1:23
~~~

Telnet server with TLS client authentication.

~~~ bash
openssl req -x509 -new -newkey ed25519 -sha256 -days 3650 -subj '/CN=example.com' -keyout ./ca.key -out ./ca.crt -nodes
openssl req -new -newkey ed25519 -sha256 -subj '/CN=srv01.example.com' -keyout ./srv01.key -out ./srv01.csr -nodes
openssl x509 -req -sha256 -days 3650 -CA ./ca.crt -CAkey ./ca.key -CAcreateserial -in ./srv01.csr -out ./srv01.crt
cat ./srv01.key ./srv01.crt > ./srv01.pem
chmod 0600 ./*.key ./*.pem
socat openssl-listen:23,reuseaddr,fork,verify=1,cafile=./ca.crt,cert=./srv01.pem exec:/bin/bash,pty,ctty,login,setsid,setpgid,stderr
~~~

Telnet client with mutual TLS authentication.

~~~ bash
openssl req -new -newkey ed25519 -sha256 -subj '/CN=example.com' -keyout ./client.key -out ./client.csr -nodes
openssl x509 -req -sha256 -days 3650 -CA ./ca.crt -CAkey ./ca.key -CAcreateserial -in ./client.csr -out ./client.crt
cat ./client.key ./client.crt > ./client.pem
chmod 0600 ./*.key ./*.pem
socat stdio,raw,echo=0 openssl:srv01.example.com:23,verify=1,cafile=./ca.crt,cert=./client.pem
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
