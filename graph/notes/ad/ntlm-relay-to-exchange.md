---
title: NTLM Relay to Exchange
---

[[notes/network/microsoft-exchange]] Web Services (EWS) can be used as [[notes/ad/ntlm-relay-sink]] [[notes/ad/ntlm-relay-to-http|over HTTP]].

Since February 2024 *Extended Protection for Authentication* aka *Channel Binding* is enabled by default on Exchange servers ([source](https://twitter.com/arekfurt/status/1757949632447955116)), but this requires an end-to-end TLS connection from the client to the server.
If a load balancer or reverse proxy is present, it must use exactly the same certificate as the Exchange server ([source](https://web.archive.org/web/20240218213505/https://www.msxfaq.de/windows/iis/iis_extended_protection.htm)).

Untested tools:

- [NtlmRelayToEWS](https://github.com/Arno0x/NtlmRelayToEWS)
- [ExchangeRelayX](https://github.com/quickbreach/ExchangeRelayX)

References:

- [One-click to OWA](https://docs.google.com/presentation/d/e/2PACX-1vRs7E1gthtfjHzhbSKEJjnrJF_8AJNRb0RTphg73erQk6dnTc_DXXLbNvPzzKj3tYc82MJdhpf1O5Kq/embed?start=false&loop=false&delayms=3000&slide=id.p1)
