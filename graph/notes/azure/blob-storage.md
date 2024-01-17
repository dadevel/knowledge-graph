---
title: Blob Storage
---

[[notes/azure/index]] Blob Storage provides object storage comparable to AWS S3.

Resources types:

- storage account: unique namespace across Azure, can be accessed over HTTP or HTTPS
    - container: folders in the storage account
        - blob: files in a container, three types *Block*, *Append* and *Page*

Authorization options:

- user, group or other identities based in Entra
- Shared Key: provides full access to storage account
- Shared Access Signature (SAS): time limited and specific permissions
- public access level
    - private: no anonymous access (default)
    - blob: only files, path must be guessed
    - container: files and directory listing

Look out for the following domains in your proxy history when you browser web applications of your target:

~~~
*.blob.core.windows.net
*.file.core.windows.net
*.table.core.windows.net
*.queue.core.windows.net
~~~

See [[notes/recon/azure]] for DNS subdomain brute forcing on this domains.

Check [grayhatwarfare.com](https://buckets.grayhatwarfare.com/buckets) for public blob storage containers.

The default name for CloudShell storage accounts matches the regex `^cs-[{]?[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}[}]?$`.
Storage accounts containing the strings `cs` or `shell` are likely used for CloudShell as well.

Brute force container names.

~~~ bash
ffuf -c -w ~/projects/github/wordlists/seclists/Discovery/Web-Content/common.txt -u 'https://defcorpcommon.blob.core.windows.net/FUZZ?restype=container'
~~~

List files in a container if allowed.

~~~ bash
curl -sSf 'https://defcorpcommon.blob.core.windows.net/backup?restype=container&comp=list' | xq -r .EnumerationResults.Blobs.Blob.Name
~~~

Otherwise brute force paths.

~~~ bash
ffuf -c -w ~/projects/github/wordlists/seclists/Discovery/Web-Content/common.txt -u 'https://defcorpcommon.blob.core.windows.net/backup/FUZZ' -e .cfg,.conf,.config,.json,.yml,.yaml,.xml,.html,.bak -recursion -recursion-depth 3 -v
~~~

Download a file.

~~~ bash
curl -sSf 'https://defcorpcommon.blob.core.windows.net/backup/blob_client.py'
~~~

Example SAS URL: <https://defcorpcodebackup.blob.core.windows.net/client?sp=rl&st=2023-09-28T13:23:54Z&se=2024-09-30T21:23:54Z&sv=2022-11-02&sr=c&sig=fpfANtrMtI0Zo2x5IclJ8Ca4K794NA18rUvDN%2FHuRTk%3D>

If `curl`ing the SAS URL fails with *access denied*, try opening it as *Blob Container* in [Azure Storage Explorer](https://azure.microsoft.com/en-us/products/storage/storage-explorer).

Authenticated enumeration of a Storage Account with Azure CLI.

~~~ bash
az storage account list | jq -r '.[].name'
az storage container list --account-name corppbackup | jq -r '.[].name'
az storage blob list --account-name corppbackup --container-name documents | jq -r '.[].name'
az storage blob download --account-name corppbackup --container-name documents --name passwords.csv
~~~

Untested tools:

- [goblob](https://github.com/macmod/goblob)

References:

- [Exploring the Dark Side of Package Files and Storage Account Abuse](http://web.archive.org/web/20231025190319/https://3xpl01tc0d3r.blogspot.com/2023/10/exploring-dark-side-of-package-files.html)
- [Azure privilege escalation via Cloud Shell](http://web.archive.org/web/20221103130917/https://www.netspi.com/blog/technical/cloud-penetration-testing/attacking-azure-cloud-shell/). exfiltrate tokens from Cloud Shell with write access to underlying Storage Account
- [Privilege escalation via storage accounts](http://web.archive.org/web/20231028184610/https://scribe.rip/@rogierdijkman/privilege-escalation-via-storage-accounts-bca24373cc2e), escalate from Storage Account to Function App
