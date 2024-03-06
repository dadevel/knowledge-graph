---
title: Public M365 Groups
---

By default every user can create [[notes/m365/index]] groups and by default this groups are public.
This means that associated [[notes/m365/exchange]] mailboxes, [[notes/m365/sharepoint]] folders and [[notes/m365/onenote]] notebooks are public as well.

Open [myapps.microsoft.com](http://myapps.microsoft.com), select the *People* application, select *All distribution lists* and check if any public group has a *Files* tab ([source](https://twitter.com/EricaZelic/status/1711825153854759346)).
You can also check the *public?* column in [[notes/tools/roadtools]].

Also check for public teams in [[notes/m365/teams]].
They are M365 groups under the hood.
The *General* channel can always be read by all members of a team ([source](https://twitter.com/ianmoran/status/1711850556614979716))

Open [account.activedirectory.windowsazure.com](https://account.activedirectory.windowsazure.com/r#/groups) to list, join and edit M365 groups ([source](http://web.archive.org/web/20230608000655/https://clement.notin.org/blog/2021/03/01/risks-of-microsoft-teams-and-microsoft-365-groups/)).

You can list public groups with [[notes/tools/roadtools]].

~~~ bash
sqlite3 ./roadrecon.db 'SELECT displayName FROM Groups WHERE isPublic';
~~~
