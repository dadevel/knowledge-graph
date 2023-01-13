---
title: LSASS Dump
---

[[notes/windows/credential-access-admin]]

The LSASS process caches NT hashes of users that recently logged in on the system.
Dumping the process requires local admin rights and [[notes/windows/privilege-debug]].

After dumping the process successfully, transfer the dump file to your machine and [[notes/windows/lsass-dump-extraction|extract the secrets]].

> **OpSec:**
> Every EDR tries to detect LSASS dumps.
> Is is better to avoid it all together and use techniques like [[notes/ad/token-impersonation]] instead.

References:

- [Function map of LSASS dump techniques](https://cartographer.run/library_v2?technique_id=2&proc_id=2)
- [LSASS dumping in 2021/2022](http://web.archive.org/web/20221110062337/https://s3cur3th1ssh1t.github.io/Reflective-Dump-Tools/)
