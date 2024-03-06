---
title: Phishing via Email
---

Services:

- [Message Header Analyzer](https://mha.azurewebsites.net/pages/mha.html), official Microsoft
- [emailspooftest.com](https://emailspooftest.com/toolbox.aspx), send example phishing emails to your own mailbox

Untested tools:

- [EmailFlare](https://github.com/giuseppelt/emailflare), send mails trough CloudFlare and MailChannel for free
- [SpamChannel](https://github.com/byt3bl33d3r/SpamChannel), for 80$ as MailChannel customer spoof emails from any other customer trough Cloudflare Workers

References:

- [twitter.com/rogue_kdc/status/1190358489434116097](https://twitter.com/rogue_kdc/status/1190358489434116097), setup catch-all mail on look-alike phishing domains, you might catch mails by people who misspelled the domain
- [Spoofing calendar invites using .ics files](http://web.archive.org/web/20220930075016/https://mrd0x.com/spoofing-calendar-invites-using-ics-files/), also see [twitter.com/delivr_to/status/1613290789320396800](https://twitter.com/delivr_to/status/1613290789320396800)
- [Real or fake? How to spoof email](http://web.archive.org/web/20221006094641/https://www.trustedsec.com/blog/real-or-fake-how-to-spoof-email/)
- [Awesome Emails](https://github.com/jonathandion/awesome-emails), list of resources to build better HTML emails

# Discovery

Send an email to a nonexistent email address and check the email headers of the *nondelivery notification*:

- verdict of spam protection appliances in the delivery path (optimize your phishing email until it is no longer detected)
- on-prem mail server or Exchange Online
- SPF and DKIM validation

Untested tools:

- [Phishious](https://github.com/CanIPhish/Phishious), looks promising
- [ThePhish](https://github.com/emalderson/ThePhish), automated phishing email analysis, complex
- [decode-spam-headers](https://github.com/mgeeky/decode-spam-headers)

# Against M365

Outlook doesn't let you click links that contain credentials, but this can be bypassed with a `<base>` tag.
Furthermore it is possible to show a fake domain in the link preview of `<a>` tags ([source](https://twitter.com/ldionmarcil/status/1661792459012075520))

~~~ html
<div>
  <base href="https://fake.com&#x200A;&#x0338;@v2">
  <a href="archive.zip">click me</a>
  <!-- displayed as https://fake.com/@v2/archive.zip, opens https://archive.zip -->
</div>
~~~

References:

- [Speedrun for a O365 Phishing infrastructure](https://web.archive.org/web/20231205060205/https://badoption.eu/blog/2023/12/03/PhishingInfra.html), use free dev tenant
- [Next Gen Phishing - Leveraging Azure Information Protection](http://web.archive.org/web/20220703195955/https://www.trustedsec.com/blog/next-gen-phishing-leveraging-azure-information-protection/)
- [Blocked attachments in Outlook](https://support.microsoft.com/en-us/office/blocked-attachments-in-outlook-434752e1-02d3-4e90-9124-8b81e49a8519)

# Exchange Online Direct Send

SPF and DKIM checks fail, but the email gets delivered to the recipients inbox nevertheless.
Only malware filtering still applies.

~~~ bash
swaks -s corp-com.mail.protection.outlook.com -f satya.nadella@microsoft.com -t john.doe@corp.com --header 'Subject: Test' --add-header 'MIME-Version: 1.0' --body 'This is totally legit.'
~~~

References:

- [Spoofing Microsoft 365 Like It’s 1995](http://web.archive.org/web/20231024041451/https://www.blackhillsinfosec.com/spoofing-microsoft-365-like-its-1995/) and [Spamming Microsoft 365 Like It’s 1995](http://web.archive.org/web/20231220123638/https://www.blackhillsinfosec.com/spamming-microsoft-365-like-its-1995/)

# Spoofed sender from secondary domains

If customer sends emails from `corp.com`, but also has `corp.de` registered, check for SPF records on `corp.de`.
If SPF is missing, which it probably will, try sending phishing mails from e.g. `hr@corp.de`.

# SMTP Smuggling

Untested tools:

- [SMTP-Smuggling-Tools](https://github.com/the-login/smtp-smuggling-tools)
- [smtpsmug](https://github.com/hannob/smtpsmug)

References:

- [SMTP Smuggling - Spoofing E-Mails Worldwide](http://web.archive.org/web/20231229194346/https://sec-consult.com/blog/detail/smtp-smuggling-spoofing-e-mails-worldwide/)
