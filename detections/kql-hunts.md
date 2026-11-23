# Microsoft Defender XDR - KQL hunts

Tables and functions used here (`EmailEvents`, `EmailUrlInfo`, `UrlClickEvents`, `EntraIdSignInEvents`, `DeviceNetworkEvents`, `ipv4_is_in_any_range()`, `ipv6_is_in_any_range()`, `parse_ipv6_mask()`, `externaldata`) are documented on Microsoft Learn. Run each hunt in Advanced Hunting with the time picker set to 30 days.

Two ways to load the indicators:
- **Live:** `externaldata` pulls the CSVs from this repository, so the hunts stay current.
- **Inline:** paste the lists below, for tenants that block outbound fetches.

## H1 - Inbound mail from fleet IPs or domains (live lists)

```kusto
let FleetIPs = externaldata(ip:string, provider:string, asn:string, smtp_banner_hostname:string, tls_cert_cn:string, last_seen_utc:string)
    [@"https://raw.githubusercontent.com/yankywilson/mx-server-fleet-cti/main/iocs/fleet-ips.csv"] with (format="csv", ignoreFirstRecord=true)
    | project ip;
let FleetDomains = externaldata(domain:string, cert_families:string, registrar:string, created_utc:string, dns_host:string)
    [@"https://raw.githubusercontent.com/yankywilson/mx-server-fleet-cti/main/iocs/domains.csv"] with (format="csv", ignoreFirstRecord=true)
    | project domain;
EmailEvents
| where SenderIPv4 in (FleetIPs) or SenderFromDomain in (FleetDomains) or SenderMailFromDomain in (FleetDomains)
| project Timestamp, RecipientEmailAddress, SenderFromAddress, SenderMailFromDomain, SenderIPv4, Subject, DeliveryAction, DeliveryLocation, ThreatTypes, NetworkMessageId
| order by Timestamp desc
```

## H2 - Inbound mail from fleet netblocks (inline)

```kusto
let FleetNets = dynamic(["31.77.120.0/24","216.158.220.0/24","151.242.139.0/24","77.67.28.0/24","94.158.184.0/24","212.69.8.0/24","89.40.83.0/24","206.232.102.0/24","222.167.237.0/24","194.104.138.0/24","54.36.174.217/32","54.36.174.220/32","54.36.174.236/32","54.36.175.25/32","65.109.58.141/32","79.137.69.148/32","79.137.70.8/32","79.137.70.17/32","79.137.70.34/32","95.216.122.225/32","95.216.122.226/32","95.216.122.227/32","95.216.122.228/32","95.216.122.229/32","95.216.122.230/32","95.216.122.231/32","95.216.122.232/32","95.216.122.233/32","95.216.122.234/32","95.216.122.235/32","95.216.122.236/32","95.216.122.237/32","95.216.122.238/32","95.216.122.239/32","95.216.122.240/32","95.216.122.241/32","95.216.122.242/32","95.216.122.243/32","95.216.122.244/32","95.216.122.245/32","95.216.122.246/32","95.216.122.247/32","95.216.122.248/32","95.216.122.249/32","95.216.122.250/32","95.216.122.251/32","95.216.122.252/32","95.216.122.253/32","155.254.21.125/32","155.254.21.134/32","155.254.21.182/32","155.254.21.184/32","155.254.21.185/32","155.254.21.186/32","155.254.21.187/32","155.254.21.188/32","155.254.21.189/32","155.254.25.73/32","155.254.29.60/32","155.254.29.61/32","155.254.29.62/32","155.254.29.64/32","155.254.29.106/32","155.254.29.107/32","155.254.29.114/32","155.254.29.115/32","155.254.29.156/32","155.254.29.157/32","155.254.29.159/32","155.254.29.160/32","155.254.30.41/32","155.254.30.42/32","155.254.30.44/32","155.254.30.45/32","155.254.30.46/32","155.254.30.47/32","155.254.30.253/32","155.254.31.164/32","192.154.253.233/32","192.158.225.170/32","192.158.230.39/32","192.158.230.41/32","192.158.230.42/32","192.158.230.43/32","192.158.230.44/32","192.158.230.45/32","192.158.230.46/32","192.158.230.47/32","192.158.230.48/32","192.158.230.49/32","192.158.230.50/32","192.158.232.62/32","192.158.232.126/32","192.158.232.222/32","192.158.238.146/32","192.158.238.148/32","192.158.238.157/32","15.204.194.100/32","95.216.122.254/32"]);
EmailEvents
| where ipv4_is_in_any_range(SenderIPv4, FleetNets)
| summarize Emails = count(), Recipients = dcount(RecipientEmailAddress), Subjects = make_set(Subject, 10), Actions = make_set(DeliveryAction) by SenderIPv4, SenderFromDomain
| order by Emails desc
```

## H3 - Links to fleet domains in mail

```kusto
let FleetDomains = dynamic(["adamsethfox.com","agriprofession.com","allmideast.com","andoverlimousine.com","bajaflyfishers.com","basproshops.com","benitoregalado.com","boltonbelgium.com","braxtonfreightway.com","breathworkeurope.com","calicater.com","carryhandbags.com","cashadvancedloan.com","ccdclass.com","collectorclocks.com","colordesignfinishes.com","copperfieldgifts.com","curveddrives.com","davidquinton.com","devriendenvanjacob.com","dockilockennel.com","eastcapeflyfishers.com","entertainmentarmoires.com","facelessjuggs.com","floorproasia.com","flyingdistances.com","freehomealarmsystem.com","gingerbreadbarn.com","godjehovah.com","godsbarn.com","gourmethazelnuts.com","greenguardcovers.com","heavyequipmentadjusters.com","hedgefundsinfo.com","herondetox.org","hidefswingers.com","informationssystems.com","inotarypublic.com","jeffersondairy.com","jonesdeliveryservice.com","kabirbakery.com","levantbureau.com","listcellboard.com","lockboxdirectory.com","luciusashields.com","maiersbakery.com","marylandcrabcakedelivery.com","mightenyip.com","milspecmagnetics.com","musclecaradz.com","newtechnologiessolutions.com","newyorkseniornews.com","norforkdesign.com","ontariotablesoccer.com","overseasadventuretours.com","panasafety.com","phoenixseniornews.com","pittsburghpostgazete.com","quadramail.com","racksalesonline.com","rcparagliders.com","realestateinandover.com","relaxingzones.com","richardtoddhunter.com","rideaucliffe.com","roscoweb.com","saavytravel.com","scraigslist.com","seattleseniornews.com","sewardmonsonandassoc.com","sharewarehaven.com","solardons.com","stickfigureballet.com","straightmembers.com","superbrushfoamswabs.net","tasteoftheamazon.com","thinkgreenbuilders.com","tiajuanaflats.com","tianismusic.com","topazromance.com","verginmoney.com","vixensgalleries.com","vsrwhitefish.com","wanttomeetyou.com","wholesalesilverchains.com","womandentists.com","womendentistsjournal.com","worlddriverchampion.com","wwwasswatcher.com","wwwpricechopper.com","xfactorfilms.com","zoomergtm.co","reedjordan.com"]);
EmailUrlInfo
| where UrlDomain has_any (FleetDomains)
| join kind=inner (EmailEvents | project NetworkMessageId, RecipientEmailAddress, SenderFromAddress, Subject, DeliveryAction) on NetworkMessageId
| project Timestamp, RecipientEmailAddress, SenderFromAddress, Subject, Url, UrlDomain, DeliveryAction
```

## H4 - Clicks on fleet domains

```kusto
let FleetDomains = dynamic(["adamsethfox.com","agriprofession.com","allmideast.com","andoverlimousine.com","bajaflyfishers.com","basproshops.com","benitoregalado.com","boltonbelgium.com","braxtonfreightway.com","breathworkeurope.com","calicater.com","carryhandbags.com","cashadvancedloan.com","ccdclass.com","collectorclocks.com","colordesignfinishes.com","copperfieldgifts.com","curveddrives.com","davidquinton.com","devriendenvanjacob.com","dockilockennel.com","eastcapeflyfishers.com","entertainmentarmoires.com","facelessjuggs.com","floorproasia.com","flyingdistances.com","freehomealarmsystem.com","gingerbreadbarn.com","godjehovah.com","godsbarn.com","gourmethazelnuts.com","greenguardcovers.com","heavyequipmentadjusters.com","hedgefundsinfo.com","herondetox.org","hidefswingers.com","informationssystems.com","inotarypublic.com","jeffersondairy.com","jonesdeliveryservice.com","kabirbakery.com","levantbureau.com","listcellboard.com","lockboxdirectory.com","luciusashields.com","maiersbakery.com","marylandcrabcakedelivery.com","mightenyip.com","milspecmagnetics.com","musclecaradz.com","newtechnologiessolutions.com","newyorkseniornews.com","norforkdesign.com","ontariotablesoccer.com","overseasadventuretours.com","panasafety.com","phoenixseniornews.com","pittsburghpostgazete.com","quadramail.com","racksalesonline.com","rcparagliders.com","realestateinandover.com","relaxingzones.com","richardtoddhunter.com","rideaucliffe.com","roscoweb.com","saavytravel.com","scraigslist.com","seattleseniornews.com","sewardmonsonandassoc.com","sharewarehaven.com","solardons.com","stickfigureballet.com","straightmembers.com","superbrushfoamswabs.net","tasteoftheamazon.com","thinkgreenbuilders.com","tiajuanaflats.com","tianismusic.com","topazromance.com","verginmoney.com","vixensgalleries.com","vsrwhitefish.com","wanttomeetyou.com","wholesalesilverchains.com","womandentists.com","womendentistsjournal.com","worlddriverchampion.com","wwwasswatcher.com","wwwpricechopper.com","xfactorfilms.com","zoomergtm.co","reedjordan.com"]);
UrlClickEvents
| where Url has_any (FleetDomains)
| project Timestamp, AccountUpn, Url, ActionType, IPAddress, NetworkMessageId
```

## H5 - Sign-ins from fleet netblocks

```kusto
let FleetNets = dynamic(["31.77.120.0/24","216.158.220.0/24","151.242.139.0/24","77.67.28.0/24","94.158.184.0/24","212.69.8.0/24","89.40.83.0/24","206.232.102.0/24","222.167.237.0/24","194.104.138.0/24","54.36.174.217/32","54.36.174.220/32","54.36.174.236/32","54.36.175.25/32","65.109.58.141/32","79.137.69.148/32","79.137.70.8/32","79.137.70.17/32","79.137.70.34/32","95.216.122.225/32","95.216.122.226/32","95.216.122.227/32","95.216.122.228/32","95.216.122.229/32","95.216.122.230/32","95.216.122.231/32","95.216.122.232/32","95.216.122.233/32","95.216.122.234/32","95.216.122.235/32","95.216.122.236/32","95.216.122.237/32","95.216.122.238/32","95.216.122.239/32","95.216.122.240/32","95.216.122.241/32","95.216.122.242/32","95.216.122.243/32","95.216.122.244/32","95.216.122.245/32","95.216.122.246/32","95.216.122.247/32","95.216.122.248/32","95.216.122.249/32","95.216.122.250/32","95.216.122.251/32","95.216.122.252/32","95.216.122.253/32","155.254.21.125/32","155.254.21.134/32","155.254.21.182/32","155.254.21.184/32","155.254.21.185/32","155.254.21.186/32","155.254.21.187/32","155.254.21.188/32","155.254.21.189/32","155.254.25.73/32","155.254.29.60/32","155.254.29.61/32","155.254.29.62/32","155.254.29.64/32","155.254.29.106/32","155.254.29.107/32","155.254.29.114/32","155.254.29.115/32","155.254.29.156/32","155.254.29.157/32","155.254.29.159/32","155.254.29.160/32","155.254.30.41/32","155.254.30.42/32","155.254.30.44/32","155.254.30.45/32","155.254.30.46/32","155.254.30.47/32","155.254.30.253/32","155.254.31.164/32","192.154.253.233/32","192.158.225.170/32","192.158.230.39/32","192.158.230.41/32","192.158.230.42/32","192.158.230.43/32","192.158.230.44/32","192.158.230.45/32","192.158.230.46/32","192.158.230.47/32","192.158.230.48/32","192.158.230.49/32","192.158.230.50/32","192.158.232.62/32","192.158.232.126/32","192.158.232.222/32","192.158.238.146/32","192.158.238.148/32","192.158.238.157/32","15.204.194.100/32","95.216.122.254/32"]);
EntraIdSignInEvents
| where ipv4_is_in_any_range(IPAddress, FleetNets)
| project Timestamp, AccountUpn, IPAddress, Application, UserAgent, ErrorCode, Country
| order by Timestamp desc
```

## H6 - Azure AD PowerShell with an empty or bare user agent (toolset A)

Behaviour hunt. It does not depend on any IP list, so it still works after the exits rotate.

```kusto
// Azure Active Directory PowerShell, app ID 1b730954-1685-4b74-9bfd-dac224a7b894
EntraIdSignInEvents
| where ApplicationId == "1b730954-1685-4b74-9bfd-dac224a7b894"
| where isempty(UserAgent) or UserAgent == "Mozilla/5.0"
| summarize Attempts = count(), Accounts = dcount(AccountUpn), Codes = make_set(ErrorCode),
            First = min(Timestamp), Last = max(Timestamp) by IPAddress, UserAgent, Country
| order by Attempts desc
```

**Tuning.** Admin scripts can use this app. Real admin sessions usually send a full PowerShell user agent. Exclude known admin IPs before you alert.

## H7 - Go HTTP client or a stale Edge 130 string against the Azure Portal (toolset B)

```kusto
// Azure Portal, app ID c44b4083-3bb0-49c1-b47d-974e53cbdf3c
EntraIdSignInEvents
| where ApplicationId == "c44b4083-3bb0-49c1-b47d-974e53cbdf3c"
| where UserAgent startswith "Go-http-client"
     or (UserAgent has "Edg/130.0.0.0" and UserAgent has "OS/10.0.26100")
| summarize Attempts = count(), Accounts = dcount(AccountUpn), Codes = make_set(ErrorCode),
            First = min(Timestamp), Last = max(Timestamp) by IPAddress, UserAgent
| order by Attempts desc
```

**Tuning.** No browser sends `Go-http-client`. The Edge string is a weaker signal: confirm with the IP ranges in H8.

## H8 - Sign-ins from the IPv6 lease batch and related exit ranges

```kusto
let ExitNets6 = dynamic(["2602:fad4:17::/48","2602:fad4:18::/45","2602:fad4:20::/45","2602:fad4:28::/47","2a0d:4b40::/29","2a0a:7e00::/29"]);
EntraIdSignInEvents
| where IPAddress contains ":"
| where ipv6_is_in_any_range(IPAddress, ExitNets6)
| summarize Attempts = count(), Accounts = dcount(AccountUpn), Apps = make_set(Application),
            Agents = make_set(UserAgent, 5), Codes = make_set(ErrorCode),
            First = min(Timestamp), Last = max(Timestamp) by Prefix48 = parse_ipv6_mask(IPAddress, 48)
| order by Attempts desc
```

The four `2602:fad4` entries are the shortest cover of the 19 × /48 batch (2602:fad4:17::/48 – 2602:fad4:29::/48).

## H9 - Any contact with the 8 OVH servers or their fronts

```kusto
let Servers = dynamic(["54.36.174.217","79.137.70.8","79.137.69.148","54.36.175.25","79.137.70.34","54.36.174.220","54.36.174.236","79.137.70.17"]);
let Fronts = dynamic(["212.69.8.0/24","89.40.83.0/24","77.67.28.0/24","194.104.138.0/24","151.242.139.0/24","222.167.237.0/24","31.77.120.0/24","94.158.184.0/24"]);
union
    (EntraIdSignInEvents
        | where IPAddress in (Servers) or ipv4_is_in_any_range(IPAddress, Fronts)
        | project Timestamp, Source = "SignIn", Ip = IPAddress, Who = AccountUpn, Detail = strcat(Application, " | ", ErrorCode)),
    (EmailEvents
        | where SenderIPv4 in (Servers) or ipv4_is_in_any_range(SenderIPv4, Fronts)
        | project Timestamp, Source = "Email", Ip = SenderIPv4, Who = RecipientEmailAddress, Detail = strcat(SenderFromAddress, " | ", DeliveryAction)),
    (DeviceNetworkEvents
        | where RemoteIP in (Servers) or ipv4_is_in_any_range(RemoteIP, Fronts)
        | project Timestamp, Source = "Network", Ip = RemoteIP, Who = DeviceName, Detail = strcat(InitiatingProcessFileName, " -> ", RemotePort))
| order by Timestamp desc
```

**Priority.** A hit on a server's native IP is stronger than a hit on a front /24, because the fronts can change tenants.

## Notes

- The eight OVH BYOIP /24s were re-leased after 2026-11-12. Treat hits after that date with care.
- Hetzner 95.216.122.0/24 has other tenants, so it is listed by single IPs only.
- Advanced Hunting keeps 30 days. For older data, run the same logic in Sentinel against `SigninLogs`, with `AppId`, `UserAgent`, `IPAddress` and `ResultType`.
- Run one hunt at a time. Advanced Hunting runs only the query block that holds the cursor.
