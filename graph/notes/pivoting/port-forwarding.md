---
title: Port Forwarding
---

[[notes/pivoting/index]] by forwarding connections across network boundaries.

# Windows

`netsh` is built into Windows and has the benefit that connections are established by `svchost.exe`, but configuration requires local admin privileges.

Forward port 4455 on the local system to an internal SMB server.

~~~ bat
netsh.exe interface portproxy add v4tov4 listenport=4455 connectaddress=192.168.1.110 connectport=445
netsh.exe advfirewall firewall add rule name="allow 4455" protocol=tcp dir=in localport=4455 action=allow
~~~

When you don't have admin privileges expose the port with [[notes/tools/powercat]] in PowerShell.
Make sure to choose a listen port that is not blocked by firewall rules.

~~~ powershell
powercat -l -p 4455 -r tcp:192.168.1.110:445
~~~

# Linux

Use the builtin firewall as `root` on Linux to forward a port.
In the example below `192.0.2.1:4455` is forwarded to `192.168.1.110:445`.

=== "iptables"
    ~~~ bash
    iptables -t nat -A PREROUTING -d 192.0.2.1 -p tcp --dport 4455 -j DNAT --to-destination 192.168.1.110:445
    iptables -t nat -A POSTROUTING -d 192.168.1.110 -j MASQUERADE
    iptables -t filter -A FORWARD -d 192.168.1.110 -p tcp --dport 445 -j ACCEPT
    ~~~

=== "nftables"
    ~~~ bash
    nft add table inet nat
    nft add chain inet nat prerouting '{' type nat hook prerouting priority '-100' '}'
    nft add chain inet nat postrouting '{' type nat hook postrouting priority 100 '}'
    nft add rule inet nat prerouting ip daddr 192.0.2.1 tcp dport 4455 dnat to 192.168.1.110:445
    nft add rule inet nat postrouting ip daddr 192.168.1.110 masquerade
    nft add table inet filter
    nft add chain inet filter forward '{' type filter hook forward priority 0 '}'
    nft add rule inet filter forward ip daddr 192.168.1.110 tcp dport 445 accept
    ~~~

If you are not `root` you can forward ports in userspace, for example with [[notes/tools/socat]].
Make sure to choose a listen port that is not blocked by firewall rules.

~~~ bash
socat tcp-listen:4455,reuseaddr,fork tcp:192.168.1.110:445
~~~
