---
title: LSASS Dump against Defender Attack Surface Reduction
---

[[notes/windows/lsass-dump]] while the Windows Defender Attack Surface Reduction rule *Block credential stealing from the Windows local security authority subsystem* is enabled.
This also blocks custom *Security Support Providers* like the [[notes/tools/mimikatz]] `misc:memssp` module ([source](http://web.archive.org/web/20230530211030/https://emptydc.com/2022/06/08/windows-credential-dumping/)).

References:

- [Windows Defender LSASS ASR Exclusion Paths from 08.30.2023](http://web.archive.org/web/20231120155547/https://gist.githubusercontent.com/adamsvoboda/9ac52548d3d81f3185e36b9f0be31990/raw/db2ab39241d112342f42bbd4f80ce058673aa207/gistfile1.txt)
