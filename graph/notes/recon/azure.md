---
title: Azure Reconnaissance
---

Unauthenticated [[notes/recon/index]] in [[notes/azure/index]].

Get basic tenant info.
The tool is not yet released publicly.
Until then you can use `Invoke-AADIntReconAsOutsider` from [[notes/tools/aadinternals]] or [[notes/tools/trevorspray]] instead.

~~~ bash
poetry run python3 ./azureutils/recon.py defcorphq.onmicrosoft.com
~~~

Find Azure resources belonging to the target organization trough DNS subdomain brute forcing of Azure domains with [[notes/tools/puredns]].
This is similar to `Invoke-EnumerateAzureSubDomains` from [[notes/tools/microburst]], but with much better performance.

~~~ bash
poetry run python3 ./azureutils/dnsbrute.py defcorphq -w ./azureutils/data/dnswords.txt | tee ./dnswordlist.txt | wc -l
sudo docker run -it --rm --network host -v /srv/data:/data:ro -v "$PWD:/workdir" -u root ghcr.io/dadevel/puredns resolve /workdir/dnswordlist.txt --rate-limit 5000 --resolvers /data/trickest-resolvers.txt
~~~

Find websites that redirect to Azure login and check whether they are [[notes/recon/azure-multi-tenant-apps]].

While browsing websites check for connections to Azure domains (e.g. [[notes/azure/blob-storage]]) in your proxy history.

References:

- [PingCastle tenant resolution](https://tenantresolution.pingcastle.com/), search for tenant by id or domain
- [Azure AD recon with OSINT tools - DEF CON 31 Recon Village](https://www.youtube.com/watch?v=4NpT78zxZEo)
- [Pentesting Azure: Recon Techniques](http://web.archive.org/web/20230331072228/https://securitycafe.ro/2022/04/29/pentesting-azure-recon-techniques/)
