---
title: Windows Privileges
---

Dangerous privileges that allow [[notes/windows/escalation]].
Virtual (local) service accounts can often abuse them to escalate to system.

![Windows privileges ([source](https://twitter.com/fr0gger_/status/1379465943965909000/))](./privileges.jpg)

References:

- [Abusing token privileges for LPE](http://web.archive.org/web/20230129105710/https://raw.githubusercontent.com/hatRiot/token-priv/master/abusing_token_eop_1.0.txt), detailed explanation on how to exploit many privileges plus incomplete proof of concepts in [token-priv](https://github.com/hatRiot/token-priv/tree/master/poptoke/poptoke)

Untested tools:

- [Privileger](https://github.com/MzHmO/Privileger), add and remove privileges from current user, start process with adjusted privileges

# Discovery

~~~ bat
whoami /priv
~~~

In `secpol.msc` GUI under `Security Settings/Local Policies/User Rights Assignment`.

# Escalation without privileges

If the dangerous privileges of a local service account were removed you can regain them by creating a scheduled task with [FullPowers](https://github.com/itm4n/FullPowers).
