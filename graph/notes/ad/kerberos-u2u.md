---
title: U2U
---

> In the [[notes/ad/kerberos]] user-to-user protocol, one user acts as a server, and the other user acts as a client.
> At the client-user's request, the server-user sends his TGT to the client-user, who then gets credentials from the KDC, encrypted with the session keys of both TGTs.
> [source](http://www.di-srv.unisa.it/~ads/corso-security/www/CORSO-0001/kerberos/ref/kerberos-faq.html#u2uauth)

![U2U flow([source](https://i.blackhat.com/USA-22/Wednesday/US-22-Forshaw-Taking-Kerberos-To-The-Next-Level.pdf))](kerberos-u2u-flow.png)
