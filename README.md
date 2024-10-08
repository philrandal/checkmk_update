[PACKAGE]: ../../raw/master/mkp/checkmk_update-0.3.2-20240924.mkp "checkmk_update-0.3.2-20240924.mkp"
# Checkmk update 

This plugin monitors the update status of your CMK sites and your CMK appliance firmware. The plugin reads its data once a day form the Checkmk download page (**https://download.checkmk.com/stable_downloads.json**).

THX to Baris Leenders for providing the data as JSON download and Martin Hirschvogel for supporting the development of this plugin (both from tribe29).

**NOTE**: before updating from the special agent version of this plugin, remove the old package completely (rules and package) please. 

**NOTE**: to get the download URLs in the service details not replaced by CMK you need to disable `Escape HTML in service output` (_Setup_ > _Services_ > _Service monitoring rules_ > _Escape HTML in service output_) for the service `Checkmk Update`.

---
### Prerequisites

For the check plugin to work
- Your CMK site servers need to run check-mk agent version 2.0.0 or higher to get CMK site informations
- The HW/SW inventory plugin for Linux must be installed and running (`mk_inventory.linux` agent plugin needs to be deployed)
- The CMK server, where the check runs must have access to **https://download.checkmk.com/stable_downloads.json**

---
### Download

* [Download latest mkp file][PACKAGE]

**Note**: before you update to a newer version, alway check the [CHANGELOG](CHANGELOG). There might be incompatible changes.

---
### Installation

You can install the package by uploading it to your CheckMK site and as site user run 
```
mkp install PACKAGENAME-VERSION.mkp
```
or beginning with CMK2.2.x
```
mkp add PACKAGENAME-VERSION.mkp
mkp enable PACKAGENAME VERSION
```
In the non RAW editions of CheckMK you can use the GUI to install the package (_Setup_ -> _Extension Packages_ -> _Upload package_)

---
#### Want to contribute?
Nice ;-) Have a look at the [contribution guidelines](CONTRIBUTING.md "Contributing")

---
#### Check Info:

The plugin creates the service **_Checkmk Update_** with the CMK site name as the _item_

<details><summary>Montoring states</summary>

| State | condition | WATO | 
| ------ | ------ | ------ |
| CRIT | if CMK base version is older than old stable base version | yes |
| WARN | if CMK version is older than latest version of base version | yes |
| WARN | if CMK version is an old stable release | yes |
| WARN | if CMK base version could not be detected | yes |
| CRIT | if CMK appliance firmware is unsupported | yes |
| WARN | if CMK appliance firmware update is available (same base version) | yes |
| WARN | if CMK appliance firmware is not the latest release | yes |

</details>

<details><summary>Perfdata</summary>

| Metric | Unit | Perfometer | |
| ------ | ------ | ------ | ----- |
| 1.6.0 | count | no | Patchlevel of CMK version 1.6.0 |
| 2.0.0 | count | no | Patchlevel of CMK version 2.0.0 |
| 2.1.0 | count | no | Patchlevel of CMK version 2.1.0 |
| 2.2.0 | count | no | Patchlevel of CMK version 2.2.0 |

</details>

---
### WATO
<details><summary>Service monitoring rule</summary>

| Section | Rule name |
| ------ | ------ |
| Operating System Resources | Checkmk update  |

| Option | Defailt value |
| ------ | ------ |
| State if CMK base version older than old stable base version. | CRIT |
| State if CMK version is older than latest version of base version. | WARN |
| State if CMK version is an old stable release. | WARN |
| State if CMK base version could not be detected. | WARN |
| State if CMK appliance firmware is unsupported. | CRIT |
| State if CMK appliance firmware update available (same base version). | WARN |
| State if CMK appliance firmware is not the latest release. | WARN |
| Connection Timeout for update data download | 5 seconds |

</details> 

---
Sample output

![sample output](img/sample.png?raw=true "sample output")


Sample details output

![sample details output](img/sample-details.png?raw=true "sample details output")
