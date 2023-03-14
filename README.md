# Checkmk update agent [(Download the MKP package)](/../../../-/raw/master/checkmk_update.mkp "Download MKP package")

---

This plugin will check once a day if a new Checkmk version is available. The plugin reads it's data form the Checkmk download page **https://download.checkmk.com/stable_downloads.json**.

THX to Baris Leenders for providing the data as JSON download and Martin Hirschvogel for supporting the development of this plugin (both from tribe29).

**NOTE**: before updating from the special agent version of this plugin, remove the old package completely (rules and package) please. 

**NOTE**: to get the download URL not replaced by CMK you need to disable `Escape HTML in service output` (_Setup_ > _Services_ > _Service monitoring rules_ > _Escape HTML in service output_) for the service `Checkmk Update`.

---
Check Info:

* *service*: creates the service **_Checkmk Update_** with the CMK site name as the _item_
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
