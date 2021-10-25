# Checkmk update agent [(Download the MKP package)](/../../../-/raw/master/agent_checkmk_download.mkp "Download MKP package")

##### This special agent will check once a day whether a new Checkmk version is available. To use this check you need to configure the special agent "checkmk_downloads" (Setup -> Agents -> Other integrations -> Checkmk Download) on your Checkmk server. The agent reads its data form the Checkmk download URL **https://https://checkmk.com/download**.
---
Check Info:

* *service*: creates the service **_Checkmk Update_**
---
* *state*: \
    **warning**: 
    * if your Checkmk version is older than the available checkmk version for your release
    * if your Checkmk release (base version) could not be detected

    **critical**: 
    * if your Checkmk version is no longer available
---
* *wato*: none
---
* *perfdata*: none
---
* *ToDo*:
    * WATO rules
    * remove inventory
---
Sample output

![sample output](/doc/sample.png?raw=true "sample output")

Sample inventory
![sample inventory](/doc/sample_inventory.png?raw=true "sample inventory")

