---
title: Reconnaissance
---

For a first impression pass the homepage to [ssllabs.com](https://www.ssllabs.com/ssltest) or [tls.imirhil.fr](https://tls.imirhil.fr/) (hosted in Europe) and [securityheaders.com](https://securityheaders.com).

General approach:

- search the target organization on Google, note domains, physical addresses and emails
- resolve domains to IPs and look up their whois information
- search organization names and addresses in the [RIPE database](https://apps.db.ripe.net/db-web-ui/fulltextsearch), note ASNs, network ranges, locations and emails
- search for organization domains and network ranges on Shodan and Censys
- discover subdomains trough passive sources like certificate transparency logs and active DNS brute forcing

References:

- [Discovering domains via a timing attack on certificate transparency](http://web.archive.org/web/20221216191930/https://swarm.ptsecurity.com/discovering-domains-via-a-time-correlation-attack/), find domains that belong together by nearly identical certificate renewal times on [crt.sh](https://crt.sh)

Untested all-on-one solutions:

- [bbot](https://github.com/blacklanternsecurity/bbot)
- [spiderfoot](https://github.com/smicallef/spiderfoot), OSINT for threat intelligence and mapping your attack surface
- [recon-ng](https://github.com/lanmaster53/recon-ng)
- [Raccoon](https://github.com/evyatarmeged/raccoon), passive and active
- [Osmedeus](https://github.com/j3ssie/osmedeus), passive and active
- [FinalRecon](https://github.com/thewhiteh4t/finalrecon), passive and active
- even more tools and tips at [osintframework.com](https://osintframework.com)

Untested tools:

- [notify](https://github.com/projectdiscovery/notify), send stdin to Slack, Teams, etc.
- [ShadowClone](https://github.com/fyoorer/ShadowClone), massively parallelize tasks trough free FasS offerings from AWS and GCP
