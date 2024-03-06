---
title: NTLM Relay to HTTP
---

Internal and external websites with NTLM authentication can function as [[notes/ad/ntlm-relay-sink]].

A website is vulnerable if it is reachable over HTTP or if it is reachable over HTTPS and Extended Protection for Authentication (EPA) is set to `none`.
If EPA is set to `allow` or `required` it is not vulnerable.
