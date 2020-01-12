# Outlook Postmaster Query

This Python script makes it easy to discover if your outgoing SMTP server is being blocked by Microsoft's 
**Outlook.com** email infrastructure.

## Motivation

While administrating multiple small email servers, I experienced that Microsoft is pretty aggressive in their 
blacklisting of outgoing SMTP servers even though they might rarely see any traffic from them. The result is that
your users cannot reach any email addresses ending with `@hotmail.com`, `@outlook.com` and some others. Unfortunately,
Microsoft does not share why they block certain IP addresses or IP ranges. Since I don't have any problems with any
other email hosting providers whatsoever, I have to assume my SMTP servers are being unfairly targeted. I have checked
my logs every time Microsoft decided to block any of my servers' IPs, by the way. Nothing "spammy" was ever sent from
those machines.

My solution is this script that queries the API of Outlook's _Smart Network Data Service_ and alerts me if any of my
registered IPs currently being blocked by their system.

## Prerequisites

The first step is to register at Outlook.com's _Smart Network Data Service_ on their 
[website](https://sendersupport.olc.protection.outlook.com/snds/). Next, associate our IP (ranges) with your account on
the _Request Access_ tab. Now go to the _Edit Profile_ tab and click on the link to change your 
**automated access settings** under _Automated Access_. Enable automated access and save the API key that is generated.
The API key's format looks like this: `XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX`