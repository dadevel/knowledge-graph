---
title: BloodHound
---

Project: [github.com/bloodhoundad/bloodhound](https://github.com/bloodhoundad/bloodhound/)

BloodHound uses [[notes/tools/neo4j]] to visualize attack paths in AD and AAD.

# Setup

Enable *Query debug mode* in BloodHound Settings and place custom queries at `~/.config/bloodhound/customqueries.json`.

Sources for custom queries:

- <https://github.com/dadevel/bloodhoundcli/blob/main/customqueries.json>
- <https://github.com/LuemmelSec/Custom-BloodHound-Queries>
- <https://github.com/hausec/bloodhound-custom-queries>
- <https://github.com/ly4k/certipy/blob/main/customqueries.json>
- <https://github.com/compasssecurity/bloodhoundqueries>
- <https://github.com/zephrfish/bloodhound-customqueries>
- <https://github.com/mgeeky/Penetration-Testing-Tools/blob/master/red-teaming/bloodhound/Handy-BloodHound-Cypher-Queries.md>

Queries that don't return objects must be run over the [Neo4j Console](http://localhost:7474/browser/).
