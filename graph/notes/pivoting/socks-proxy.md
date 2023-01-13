---
title: SOCKS Proxy
---

[[notes/pivoting/index]] by forwarding local connections over a SOCKS proxy into a remote network.

# Linux

Use [[notes/tools/proxychains]] to redirect TCP connections of dynamically linked executables over a SOCKS proxy.

~~~ bash
mkdir ~/.proxychains
cat << EOF > ~/.proxychains/proxychains.conf
strict_chain
proxy_dns
tcp_read_time_out 1000
tcp_connect_time_out 1000

[ProxyList]
socks5 127.0.0.1 1080
EOF
proxychains -q nmap -sT 192.168.178.0/24
~~~

Untested tools:

- [tun2socks](https://github.com/xjasonlyu/tun2socks), creates Linux TUN device that sends traffic over a SOCKS proxy

# Windows

References:

- [Living Off the Foreign Land - Part 1: Setup Linux VM for SOCKS routing](http://web.archive.org/web/20230815182311/https://blog.bitsadmin.com/living-off-the-foreign-land-windows-as-offensive-platform) and [Part 2: Configuring the Offensive Windows VM](http://web.archive.org/web/20230815182322/https://blog.bitsadmin.com/living-off-the-foreign-land-windows-as-offensive-platform-part-2)
- [WireSocks for easy proxied routing](http://web.archive.org/web/20221006063538/https://sensepost.com/blog/2022/wiresocks-for-easy-proxied-routing/), route traffic from attacker Windows VM over WireGuard over tun2socks over reverse SOCKS proxy into target network
- [Proxy Windows Tooling via SOCKS](http://web.archive.org/web/20221208103441/https://scribe.rip/@spectreops/proxy-windows-tooling-via-socks-c1af66daeef3)
- [SOCKS Pivoting on Windows](https://training.zeropointsecurity.co.uk/courses/take/red-team-ops/texts/38279262-windows-tools)
