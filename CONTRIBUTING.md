# Contributing

If you have any issues or ideas for improvement you can contact me in the [CMK forum](https://forum.checkmk.com/) by sending me a direct message to `@thl-cmk` (this is the prefered way) or send an email to _thl-cmk[at]outlook[dot]com_.

Please include:
- your CMK version/edition
- your environment (stand alone or distributed)
- the OS of your CMK server(s)
- the version of the plugin
- the crash report (if any)

For agent based plugins I might need also the agent output of the plugin.

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
