---
title: "Device Code Phishing Evasion Techniques"
date: 2026-07-24
external_link: "https://github.com/PaloAltoNetworks/Unit42-timely-threat-intel/blob/main/2026-07-23-Device-code-phishing-evasion-techniques.txt"
summary: "Device-code phishing campaigns are combining CAPTCHA gates, multi-step SaaS lure chains, encrypted blob-page delivery and source-level text obfuscation to evade automated scanners and reputation checks."
tags: [Phishing, OAuth, Evasion, Web Security]
---

We observed device-code phishing campaigns using four complementary evasion techniques. CAPTCHA gates block basic URL scanners while mimicking legitimate Microsoft security checks, and multi-step flows route victims through trusted SaaS platforms before revealing the phishing page.

Other campaigns decrypt phishing HTML inside the browser and deliver it through a session-unique blob URL that blocklists cannot retrieve. The pages also disrupt content detection with Cyrillic lookalike characters, zero-width spaces and randomized strings embedded in `<bdi>` elements, while remaining visually convincing to victims.

[Read the full Unit 42 report and indicators →](https://github.com/PaloAltoNetworks/Unit42-timely-threat-intel/blob/main/2026-07-23-Device-code-phishing-evasion-techniques.txt)
