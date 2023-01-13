---
title: WDAC
---

Windows Defender Application Control

Disable WDAC policy as local admin on Windows 11 ([source](https://twitter.com/_RastaMouse/status/1663554620118142976)).

~~~ bat
citool.exe -rp "{POLICY_GUID}" -json
shutdown.exe /r /t 0
~~~

Untested tools:

- [Aladdin](https://github.com/nettitude/Aladdin), AppLocker / WDAC bypass trough .NET deserilization in `AddInProcess.exe`, see [Introducing Aladdin](http://web.archive.org/web/20230302073844/https://labs.nettitude.com/blog/introducing-aladdin/)

References:

- [Ultimate WDAC bypass list](https://github.com/bohops/ultimatewdacbypasslist/)
