---
title: M365 Persistence
---

[[notes/mitre-attack/persistence]] as unprivileged [[notes/m365/index]] user:

- invite an attacker as guest
- register an additional MFA device
- create a mailbox forwarding rule

References:

- [Security vulnerability in Azure AD & Office 365 identity federation](http://web.archive.org/web/20230605210813/https://aadinternals.com/post/federation-vulnerability/), bit misleading title, persistence by setting up ADFS trust
- [Passwordless persistence and privilege escalation in Azure](http://web.archive.org/web/20221222100649/https://scribe.rip/@specterops/passwordless-persistence-and-privilege-escalation-in-azure-98a01310be3f), persistence trough certificate-based authentication
