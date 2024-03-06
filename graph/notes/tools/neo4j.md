---
title: Neo4j
---

# Setup

Run Neo4j as container.

~~~ bash
podman run -it --rm --network host -v bloodhound-$project:/data -e NEO4J_AUTH=none docker.io/library/neo4j:4.4.12
firefox http://localhost:7474/
~~~

**Note:** As of November 2022 Neo4j v5 causes performance issues with BloodHound.

# Cypher Query Language

Match all nodes of a specific type.

~~~ cypher
MATCH (u:User) RETURN u
~~~

Match all nodes that are connect by a specific path.

~~~ cypher
MATCH p = ()-[:HasSession]->() RETURN p
~~~

`allShortestPaths` finds shortest paths for given node-edge-node pattern.

~~~ cypher
MATCH p = allShortestPaths((:User {name:'Bob'})-[r*1..]->(:Computer {name:'PC1'})) RETURN p
~~~

References:

- [Intro To Cypher](http://web.archive.org/web/20230325010225/https://blog.cptjesus.com/posts/introtocypher/)
