# Cisco NTP [(Download the MKP package)](/../../../-/raw/master/{REPLACE_WITH_PACKAGE_NAME}.mkp "Download MKP package")

Monitors status of C{REPLACE_WITH_PACKAGE_TITLE}
---
Check Info:

* *service*: creates the service **_NTP status_** and one service **_NTP {item}_** for each NTP association, with the association name/ip-address as item
---
* *state*: \
    **warning**: 
    * if NTP refID is in AUTH, AUTO, CRYPT, DENY, INIT, LOCL, RATE, STEP, TIME or XFAC (see WATO)
    * if Error counter > 0 (see WATO)

    **critical**/**warning**: 
    * if offset or stratum outside the configured levels (see WATO)\
---
* *wato*: [(see WATO options)](/../../../-/raw/master/doc/wato.png "see sample screenshot")
---
* *perfdata (if avilable)*: 
    * Offset (s)
    * Delay (s)
    * Jitter (s)
    * Protocol errors (/s)
    * Version errors (/s)
---
#### Want to contribute?
Nice ;-) Have a look at the [contribution guidelines](CONTRIBUTING.md "Contributing")
---
Sample output

![sample output](/doc/sample.png?raw=true "sample output")

WATO

![WATO options](/doc/wato.png?raw=true "WATO options")
