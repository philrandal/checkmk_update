# Contributing

If you have any issues or ideas for improvement you can send me an email to _thl-cmk[at]outlook[dot]com_.

For some fixes/improvements I migth need the raw output of the _**lnx_distro**_ and _**omd_info**_ section from the check_mk agent.

I also need to know the following:
- version/edition of check_mk you are using
- version of the check_mk agent you are using
- version/platform of the target system


```
<<<omd_info:sep(59)>>>
[versions]
version;number;edition;demo
2.0.0p29.cfe;2.0.0p29;cfe;0
[sites]
site;used_version;autostart
removed;2.0.0p29.cfe;1
<<<lnx_distro:sep(124):persist(1679171010)>>>
[[[/etc/debian_version]]]
10.13
[[[/etc/os-release]]]
PRETTY_NAME="Debian GNU/Linux 10 (buster)"|NAME="Debian GNU/Linux"|VERSION_ID="10"|VERSION="10 (buster)"|VERSION_CODENAME=buster|ID=debian|HOME_URL="https://www.debian.org/"|SUPPORT_URL="https://www.debian.org/support"|BUG_REPORT_URL="https://bugs.debian.org/"
```
