---
title: Lateral Movement
---

> [[notes/mitre-attack/tactic]] [TA0008](https://attack.mitre.org/tactics/TA0008/): The adversary is trying to move through your environment.

![Lateral movement techniques ([source](https://www.thehacker.recipes/ad/movement/ntlm))](./lateral-movement-techniques.jpg)

If you know a user's ... ([source](https://mobile.twitter.com/_nwodtuhs/status/1451510341041594377))

- AES key -> [[notes/ad/pass-the-key]]
- NT hash -> [[notes/ad/pass-the-hash]] for NTLM authentication or [[notes/ad/overpass-the-hash]] for Kerberos authentication
- TGT -> [[notes/ad/pass-the-ticket]]
- ST -> [[notes/ad/pass-the-ticket]]
- private key -> [[notes/ad/kerberos-pkinit]] for Kerberos authentication, optionally followed by [[notes/ad/unpac-the-hash]] for NTLM authentication

Windows authentication ([source](http://web.archive.org/web/20230501143904/https://attl4s.github.io/assets/pdf/Understanding_Windows_Lateral_Movements_2023.pdf)):

- local or domain account
- interactive or network / non-interactive authentication, see [[notes/windows/logon-types]]
- local access managed with [[notes/ad/token-impersonation|access tokens]], remote access managed with logon sessions

Untested tools:

- [SharpMove](https://github.com/0xthirteen/SharpMove), can use WMI, DCOM, SCM and Task Scheduler
- [pyspnego](https://github.com/jborean93/pyspnego)
- [SharpExec](https://github.com/anthemtotheego/sharpexec), implements WMIExec, SMBExec and PSExec

References:

- [Moving laterally between Azure AD joined machines](http://web.archive.org/web/20230921105218/https://scribe.rip/@talthemaor/moving-laterally-between-azure-ad-joined-machines-ed1f8871da56)
- [Give Me an E, Give Me a T, Give Me a W. What Do You Get? RPC!](https://www.akamai.com/blog/security-research/msrpc-defense-measures-in-windows-etw), detection for lateral movement over MSRPC
- [Traces of Windows remote command execution](http://web.archive.org/web/20230804175041/https://www.synacktiv.com/publications/traces-of-windows-remote-command-execution.html), how to detect various lateral movement techniques
