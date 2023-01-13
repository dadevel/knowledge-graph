---
title: Protected Process and Protected Process Light
---

[[notes/windows/index]] executables running as Protected Process or Protected Process Light must have a code signing certificates with a special EKU.
They are inaccessible even for *NT Authority\System* and *TrustedInstaller*.
EDRs use PPL to prevent there processes from being killed.

Untested tools:

- [AntimalwareBlight](https://github.com/mattifestation/AntimalwareBlight/), execute PowerShell at Antimalware-Light protection level, requires weak ELAM driver

References:

- [Living Off the Walled Garden: Abusing the Features of the Early Launch Antimalware Ecosystem - Black Hat 2022](https://www.youtube.com/watch?v=Upo5I_mK1V4)
- [PPLdump Is Dead. Long Live PPLdump!](./gabriel-landau-ppldump-is-dead-long-live-ppldump.pdf) ([source](https://drive.google.com/file/d/1Pj7hSvsj0qvegdIUvABa9KUEKOrLzu2p/view))
- [Injecting Code into Windows Protected Processes using COM - Part 2](http://web.archive.org/web/20230317054657/https://googleprojectzero.blogspot.com/2018/11/injecting-code-into-windows-protected.html)
