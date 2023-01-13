---
title: Lateral Movement with Remote Registry
---

[[notes/lateral-movement/index]] by using [MS-RRP](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-rrp/) to modify the [[notes/windows/registry]], e.g. write to one of the [Run keys](https://persistence-info.github.io/Data/run.html).

The remote registry service runs only on servers by default, but can be started on-demand on desktops.
Access requires local admin rights.
