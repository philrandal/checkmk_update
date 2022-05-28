# Checkmk update agent [(Download the MKP package)](/../../../-/raw/master/agent_checkmk_update.mkp "Download MKP package")
---

This special agent will check once a day if a new Checkmk version is available. To use this check you need to configure the special agent "checkmk_update" (Setup -> Agents -> Other integrations -> Checkmk update) on your Checkmk server. The agent reads its data form the Checkmk download page **https://download.checkmk.com/stable_downloads.json**.

THX to baris.leenders[at]tribe29 for providing the data as JSON download and martin.hirschvogel[at]tribe29 for supporting the development of this plugin

**NOTE**: before updating from the old agent_checkmk_download agent, remove the agent_checkmk_download package completely (rules and package) please. You also need to delete the `~/tmp/check_mk/cache/cmk_downloads` cache file.

**Note**: to get the download URL not replaced by CMK you might need to disable `Escape HTML in service output` (_Setup_ > _Services_ > _Service monitoring rules_ > _Escape HTML in service output_) for the service `Checkmk update`.

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
* *wato*: [(see WATO options)](/../../../-/raw/master/doc/wato.png "see WATO options")
---
* *perfdata*: Verion history

---
Sample output

![sample output](/doc/sample.png?raw=true "sample output")

WATO options (Check)

![WATO options](/doc/wato.png?raw=true "WATO options")

WATO options (Agent)

![WATO options agent](/doc/wato-agent.png?raw=true "WATO options agent")


