---
title: SSH Pivoting
---

[[notes/tunneling/index]] and [[notes/pivoting/index]] over the [[notes/network/ssh]] protocol.

The `ssh` client is preinstalled on many Linux distros and even on Windows 10.
If you have a SSH connection to your target you won't need anything else.

![[source](https://iximiuz.com/ssh-tunnels/ssh-tunnels.png)](./ssh-tunnel-overview.png)

# Local Port Forwarding

Accept TCP connections on a local port and forward them to the remote host.

~~~ bash
ssh -L [LOCAL_ADDRESS:]LOCAL_PORT:REMOTE_ADDRESS:REMOTE_PORT sshuser@192.0.2.1
~~~

# Remote Rort Forwarding

Accept TCP connections on the remote host and forward them to a local port.

~~~ bash
ssh -R [REMOTE_ADDRESS:]REMOTE_PORT:LOCAL_ADDRESS:LOCAL_PORT sshuser@192.0.2.1
~~~

On old Windows systems were `ssh.exe` is not pre-installed [Plink](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html) from PuTTY can be used instead.
Unfortunately it does not support reverse SOCKS proxies.

~~~ bat
curl.exe -O https://the.earth.li/~sgtatham/putty/latest/w64/plink.exe
cmd.exe /c echo y | .\plink.exe -ssh -R 127.0.0.1:8080:127.0.0.1:8080 -l sshuser -pw "passw0rd" -P 22 192.0.2.1
~~~

# SOCKS Proxy

Start a local [[notes/pivoting/socks-proxy]] that forwards traffic to the remote host.

~~~ bash
ssh -D [LOCAL_ADDRESS:]LOCAL_PORT sshuser@192.0.2.1
~~~

# Reverse SOCKS Proxy

Start a [[notes/pivoting/socks-proxy]] on the remote system and forward traffic to it.
Requires a modern OpenSSH client.
Can also be used for [[notes/tunneling/ssh]].

Linux:

~~~ bash
ssh -N -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -R 127.0.0.1:1080 proxy@192.0.2.1
~~~

Windows:

~~~ bat
ssh.exe -N -o UserKnownHostsFile=NUL -o StrictHostKeyChecking=no -R 127.0.0.1:1080 proxy@192.0.2.1
~~~

Append the following snippet to `/etc/ssh/sshd_config` on your server:

~~~
Match User proxy
  ForceCommand sleep infinity
  PasswordAuthentication yes
~~~

And set a password.

~~~ bash
echo "proxy:$(uuidgen -r)" | tee /dev/stderr | sudo chpasswd
~~~

# VPN Connection

Establish a VPN-like connection over SSH with [[notes/tools/sshuttle]].
Admin rights are required only on the client.

~~~ bash
sshuttle -v --method nft --disable-ipv6 -r sshuser@192.0.2.1 192.168.178.0/24
~~~
