---
title: "Device Code-based OAuth Phishing"
date: 2026-03-23
external_link: "https://github.com/PaloAltoNetworks/Unit42-timely-threat-intel/blob/9a182ab656d6163c2e582e20a5b2e3d4ba6663a2/2026-03-23-%20Device-Code-based-OAuth-Phishing.txt"
summary: "An active phishing campaign abuses Microsoft's legitimate device-code OAuth flow to capture application tokens instead of passwords. The pages combine trusted sign-in screens with obfuscation, developer-tool detection and debugger traps."
tags: [Phishing, OAuth, Web Security]
---

This active campaign abuses Microsoft's legitimate device-code OAuth flow to capture application tokens instead of passwords. Victims interact with a real Microsoft sign-in page while the attacker's infrastructure obtains the resulting token in the background.

The phishing pages combine trusted authentication flows with obfuscated payloads, developer-tool detection and debugger traps. A captured OAuth token can provide application-level access to email, files and identity data without exposing the victim's password.

[Read the full Unit 42 report and indicators →](https://github.com/PaloAltoNetworks/Unit42-timely-threat-intel/blob/9a182ab656d6163c2e582e20a5b2e3d4ba6663a2/2026-03-23-%20Device-Code-based-OAuth-Phishing.txt)
