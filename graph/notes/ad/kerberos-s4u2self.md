---
title: S4U2self
---

> The *Service for User to Self* extension allows a service to obtain a [[notes/ad/kerberos-st]] to itself on behalf of a user.
> The user is identified to the KDC using the user's name and realm.
> Alternatively, the user might be identified based on the user's certificate.
> By obtaining a ST to itself on behalf of the user, the service receives the user's authorization data in the ticket.
> [source](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-sfu/bde93b0e-f3c9-4ddf-9f44-e1453be7af5a)

S4U2self is enabled when the `TRUSTED_TO_AUTH_FOR_DELEGATION` flag in the `userAccountControl` attribute is set on the service account.
This enables [[notes/ad/constrained-delegation-with-protocol-transition]].

Requirements ([source](./roses-are-red-violets-are-blue-s4u-bamboozles-me-u2u-too-charlie-bromberg-northsec-2023.pdf)):

- if impersonated user is protected, ticket is valid but not forwardable
- if requester is not configured for [[notes/ad/constrained-delegation]], ticket is valid but not forwardable
- if requester is configured for [[notes/ad/constrained-delegation-without-protocol-transition]], ticket is valid but not forwardable

S4U2Self can be combined with [[notes/ad/kerberos-u2u]] to enable [[notes/ad/rbcd-spn-less]], [[notes/ad/unpac-the-hash]] and [[notes/ad/sapphire-ticket]] ([source](./roses-are-red-violets-are-blue-s4u-bamboozles-me-u2u-too-charlie-bromberg-northsec-2023.pdf)).
