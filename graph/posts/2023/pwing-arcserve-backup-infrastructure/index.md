---
title: Pwning Arcserve Backup Infrastructure
---

During a recent internal pentest I was asked to take a closer look at the customers backup infrastructure.
In this blog post I will describe the complete attack path from domain user to full control over Arcserve and the underlying storage.

One word of caution: This was my first contact with Arcserve, so I don't know how applicable to other environments the identified misconfigurations are.

The setup I was up against looked roughly like this:

![Diagram of the backup infrastructure](./infra-overview.png)

Arcserve backup agents were running on multiple domain-joined Windows Servers, while the central Arcserve management server was not domain-joined.
The storage was attached to the management server over iSCSI.
An additional backup server moved the data to a tape library.
The backup server, the tape library and both storage devices were isolated in a separate network.

# Discovery

After a quick Google search I knew that systems that have the backup agent installed are easily identifiable over port 8014/tcp, at least as long as permissive firewall rules are in place, because the admin portal of the agent is accessible on this port.
In addition the portal of the management server is exposed on 8015/tcp.
Furthermore I stumbled upon [CVE-2023-26258](https://www.opencve.io/cve/CVE-2023-26258) and an [accompanying writeup by MDSec](https://www.mdsec.co.uk/2023/06/cve-2023-26258-remote-code-execution-in-arcserve-udp-backup/).
But the plan to exploit this vulnerability had to be discarded, as all agents were patched recently.
Eventually, I discovered a server that my initial user could access over RDP and had the backup agent running.

# Agent Access

On this server I was surprised to discover that an unprivileged user can read the registry values `HKLM\SOFTWARE\Arcserve\Unified Data Protection\Engine\AdminUser` and `AdminPassword`.
The latter contained an encrypted password of an Arcserve service account.
But because this encryption is performed with a publicly known static key the plain password can be recovered offline with [ArcServeDecrypter.c](https://github.com/mdsecactivebreach/CVE-2023-26258-ArcServe/), which MDSec released along with the exploit for the previously mentioned CVE.
Now I was even more surprised when I realized that the service account was domain admin.

![Alternatively local admins can dump the password blob over Remote Registry with [arcserve-regkeys.py](https://github.com/mdsecactivebreach/CVE-2023-26258-ArcServe/)](./arcserve-regdump.png)

With this service account I accessed a Domain Controller and noticed the file `C:\Program Files\Arcserve\Unified Data Protection\Engine\Configuration\BackupConfiguration.xml` which was not present on the first server.
This file contained several Base64 password blobs that, after being converted to hex, could be decrypted with `ArcServeDecrypter` as well.
One of them was the password of the local administrator on the non-domain-joined Arcserve management server.

![Excerpt from BackupConfiguration.xml](./arcserve-backup-config.png)

# Database Access

As local administrator on the management server I downloaded the file `C:\Program Files\Arcserve\Unified Data Protection\Management\Configuration\db_configuration.xml`, which contained the location and credentials of the Arcserve database.
In this case the known default credentials `arcserve_udp:@rcserveP@ssw0rd` were used.
The database was a SQL Express instance running on the management server itself, but only accessible from localhost.

Once I could access the database I dumped the encrypted credentials with the following SQL query:

~~~ sql
SELECT h.ipaddress, h.rhostname, h.osdesc, c.username, c.password FROM as_edge_host AS h, as_edge_connect_info AS c WHERE h.rhostid=c.hostid ORDER BY c.hostid;
~~~

![Database dump in SQL Studio](./arcserve-mssql.png)

Decrypting all those juicy passwords with the original tool from MDSec was a bit tedious, because it had to be recomplied for each password.
Therefore I hacked together a slightly improved [ArcserveDecrypter.cpp](https://gist.github.com/dadevel/27f9a23dccaeb6968a239204f7857b94) that allowed to quickly decrypt all passwords.
This resulted in access to several critical infrastructure components like VMware vCenter and some Linux servers.

Additionally I found admin credentials for both NAS devices saved in the browser.

![Passwords saved in the browser](./browser-passwords.png)

# Storage Access

The last steps were easy, because it turned out that the Arcserve backup server had the same local administrator password as the management server.
On the backup server, admin credentials were stored in the browser again.
This time for the tape library.
And finally I had control over the entire backup infrastructure.

![Admin on tape library](./tape-library-admin.png)

# Conclusion

Ensure your backups are well protected, especially against attackers with domain admin privileges.
Don't reuse passwords, don't save critical passwords in the browser and don't give service accounts excessive privileges.

# References

- [mdsec.co.uk/2023/06/cve-2023-26258-remote-code-execution-in-arcserve-udp-backup](https://www.mdsec.co.uk/2023/06/cve-2023-26258-remote-code-execution-in-arcserve-udp-backup/)
- [github.com/mdsecactivebreach/cve-2023-26258-arcserve](https://github.com/mdsecactivebreach/cve-2023-26258-arcserve/)
