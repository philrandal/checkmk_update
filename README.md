# Checkmk update agent [(Download the MKP package)](/../../../-/raw/master/agent_checkmk_download.mkp "Download MKP package")

Monitors checkmk update status
---
Check Info:

* *service*: creates the service **_Checkmk Update_**
---
* *state*: \
    **warning**: 
    * if your Checkmk version is older than the available checkmk version for your release
    * if your Checkmk release (base version) could not be detected

    **critical**: 
    * if your Checkmk version is no longer available\
---
* *wato*: none yet
---
* *perfdata*: none
---
#### Want to contribute?
Nice ;-) Have a look at the [contribution guidelines](CONTRIBUTING.md "Contributing")
---
Sample output

![sample output](/doc/sample.png?raw=true "sample output")

Sample inventory
![sample inventory](/doc/sample_inventory.png?raw=true "sample inventory")

