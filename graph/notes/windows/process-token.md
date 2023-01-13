---
title: Process Token
---

[[notes/windows/index]] process tokens.

An *Access Token* contains the user [[notes/windows/sid]], [[notes/windows/process-integrity|integrity level]] and [[notes/windows/privilege|assigned privileges]].
Each process has a *Primary Access Token* derived from the user that started it.
Additionally individual threads can hold an *Impersonation Token*, that allows the thread to act on behalf of another user.

*Impersonation Tokens* have four levels:

- Anonymous: only allows enumeration
- Identification: only allows enumeration
- Impersonation: local impersonation
- Delegation: impersonation across the network
 
# Escalation

Elevate privileges from local admin to system by impersonating the token of a system process like `dllhost.exe`, `OfficeClickToRun.exe`, `spoolsv.exe` or `winlogon.exe`.
