#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# License: GNU General Public License v2
#
# Author: thl-cmk[at]outlook[dot]com
# URL   : https://thl-cmk.hopto.org
# Date  : 2021-12-25
#
# Checkmk update status
#
# 2021-10-26: minor fixes (removed unused prints)
# 2021-11-04: fixed missing "versions" key in "release" section
# 2021-11-17: added checkmk appliance version
# 2021-12-07: added metrics for patch release history (a little fun) maybe one day of (cache, only checks once a day)
# 2022-05-27: fixed if agent_section has wrong format
# 2022-05-28: rewritten for new json format (THX at baris.leenders[at]tribe29
#             and martin.hirschvogel[at]tribe29 for supporting the development of this plugin)
#             added download urls for latest versions
# 2023-03-18: rewritten as a "normal" check plugin (no special agent)
#             before updating to this version remove the special agent version (rules + package)
# 2023-03-19: added support for appliance firmware version
#
#
# Known issues
# for new Linux distributions (with code name) the plugin needs to be updated :-(, this will be not necessary if tribe
# moves the distro parsing in lnx_distro to the parsing function where it belongs.


# sample agent output
# {
#     "version": 1,
#     "checkmk": {
#         "2.1.0": {
#             "version": "2.1.0",
#             "release_date": 1653379969,
#             "class": "stable",
#             "editions": {
#                 "cme": {
#                     "cma-3": [
#                         "check-mk-managed-2.1.0-3-x86_64.cma",
#                         "bc05572179302ef798eea2f80aca6d6c84a453afcf3ba9daeb14b3bae1ed5243"
#
#                     "el8": [
#                         "check-mk-managed-2.1.0-el8-38.x86_64.rpm",
#                         "3821eb16e31a4aecfc31a09488e7c3c3f9097adf55c29efa0fd5bab742e431be"
#                     ],
#                     "sles15sp3": [
#                         "check-mk-managed-2.1.0-sles15sp3-38.x86_64.rpm",
#                         "7b41935ca0468dfc4217ab836d4a0b7ad982b846a5be24041ecb282ef3d131bb"
#                     ],
#                     "bullseye": [
#                         "check-mk-managed-2.1.0_0.bullseye_amd64.deb",
#                         "2003fc551b3317efbfc45d53ebd78807c07a72d90bffa9489c81ce78b5cd7e3b"
#                     ],
#                     "focal": [
#                         "check-mk-managed-2.1.0_0.focal_amd64.deb",
#                         "352e28e459fe3f1129c6d59f544b4a0a036e89a0449ead682d6960405e44e937"
#                     ],
#                     "docker": [
#                         "check-mk-managed-docker-2.1.0.tar.gz"
#                     ],
#                     ...
#                 },
#                 "cre": {
#                     ...
#                 },
#                 "cfe": {
#                     ...
#                 },
#                 "cee": {
#                     ...
#                 }
#             }
#         },
#         "2.0.0": {
#             "version": "2.0.0p25",
#             "release_date": 1653503541,
#             "class": "oldstable",
#             "editions": {
#                 "cme": {
#                     ...
#                 },
#                 "cee": {
#                     ...
#                 },
#                 "cre": {
#                     ...
#                 },
#                 "cfe": {
#                     ...
#                 }
#             }
#         },
#         "1.6.0": {
#             "version": "1.6.0p28",
#             "release_date": 1646148925,
#             "class": "oldstable",
#             "editions": {
#                 "cme": {
#                     ...
#                 },
#                 "cee": {
#                    ...
#                 },
#                 "cre": {
#                    ...
#                 },
#                 "cfe": {
#                    ...
#                 }
#             }
#         }
#     },
#     "appliance": {
#         "1.5.1": {
#             "cfw": [
#                 "cma-1.5.1.cfw",
#                 "5aa89eb62d6720d5f17a95bb7ad2014f63a8c17b421e209f8a9431aa84265144"
#             ],
#             "ova": ["virt1-1.5.1.ova",
#                     "bd1558c21458a81f36391ff682c3e9c76753c25f026c92a043b53e28e079a9f6"
#                     ],
#             "cfw_demo": [
#                 "cma-demo-1.5.1.cfw",
#                 "1d984b7ace7c1a1e288608be666dbd6e9eb44f851f9c141b6586e16ad2b88fb1"
#             ],
#             "ova_demo": [
#                 "virt1-demo-1.5.1.ova",
#                 "393796802f0ffdd6cbb2b406993746794f2cfd6605853a6a108b0ffda6e56008"
#             ]
#         },
#         "1.4.19": {
#             "cfw": [
#                 "cma-1.4.19.cfw", "008961b71df0bfde97809f6540c303776604fae742941a3781e9547b429510d4"
#             ],
#             "ova": [
#                 "virt1-1.4.19.ova", "417b9b25793a63b3bd9a56527a63ec83ad885e09712b164deea25e09b43b9565"
#             ],
#             "cfw_demo": [
#                 "cma-demo-1.4.19.cfw",
#                 "77fc0260d49d68e9bbe7eba981760ed6bd10e3cf8920f0615ade638a7379f5a3"
#             ],
#             "ova_demo": [
#                 "virt1-demo-1.4.19.ova",
#                 "fcb3aeadcd77afaefa3de1867b91090a26840689b2d920fa3a5249c196ed88b2"
#             ]
#         }
#     }
# }
#
import re
import json
import time
import os
import requests
from typing import Dict, Final, Iterable, Mapping, Optional, Tuple, List, Any
from cmk.base.plugins.agent_based.agent_based_api.v1 import (
    register,
    Result,
    State,
    Service,
    Metric,
)

from cmk.base.plugins.agent_based.agent_based_api.v1.type_defs import (
    DiscoveryResult,
    CheckResult,
    StringTable,
)

#
#  code from lnx_distro.py start
#


_KVPairs = Iterable[Tuple[str, str]]
_Line = List[str]

Section = Mapping[str, _Line]


def _parse_lnx_distro(string_table: StringTable) -> Section:
    parsed: Dict[str, List[str]] = {}
    filename = None
    for line in string_table:
        if line[0].startswith("[[[") and line[0].endswith("]]]"):
            filename = line[0][3:-3]
        elif filename is not None:
            parsed.setdefault(filename, line)
        elif filename is None:
            # stay compatible to older versions of output
            parsed.setdefault(line[0], line[1:])
    return parsed


def inv_lnx_parse_os(line: _Line) -> _KVPairs:
    for entry in line:
        if entry.count("=") == 0:
            continue
        k, v = [x.replace('"', "") for x in entry.split("=", 1)]
        if k == "VERSION_ID":
            yield "version", v
        elif k == "PRETTY_NAME":
            yield "name", v
        elif k == "VERSION_CODENAME":
            yield "code_name", v.title()
        elif k == "ID":
            yield "vendor", v.title()


_SUSE_CODE_NAMES: Final = {
    "11.2": "Emerald",
    "11.3": "Teal",
    "11.4": "Celadon",
    "12.1": "Asparagus",
    "12.2": "Mantis",
    "12.3": "Darthmouth",
    "13.1": "Bottle",
}


def inv_lnx_parse_suse(line: _Line) -> _KVPairs:
    major = line[1].split()[-1]
    if len(line) >= 3:
        patchlevel = line[2].split()[-1]
    else:
        patchlevel = "0"

    version = "%s.%s" % (major, patchlevel)

    yield "vendor", "SuSE"
    yield "version", version
    yield "name", "%s.%s" % (line[0].split("(")[0].strip(), patchlevel)

    if (code_name := _SUSE_CODE_NAMES.get(version)) is not None:
        yield "code_name", code_name


def inv_lnx_parse_redhat(line: _Line) -> _KVPairs:
    entry = line[0]
    if entry.startswith("Oracle"):
        yield from inv_lnx_parse_oracle_vm_server(line)
    else:
        parts = entry.split("(")
        left = parts[0].strip()
        # if codename "(CODENAME)" is present, list looks like
        # ['Red Hat Enterprise Linux Server release 6.7 ', 'Santiago)']
        if len(parts) == 2:
            yield "code_name", parts[1].rstrip(")")
        name, _release, version = left.rsplit(None, 2)
        if name.startswith("Red Hat"):
            yield "vendor", "Red Hat"
        yield "version", version
        yield "name", left


def inv_lnx_parse_oracle_vm_server(line: _Line) -> _KVPairs:
    parts = line[0].split(" ")
    yield "vendor", parts.pop(0)
    yield "version", parts.pop(-1)
    yield "name", " ".join(parts[:-1])


def inv_lnx_parse_lsb(line: _Line) -> _KVPairs:
    for entry in line:
        varname, value = entry.split("=", 1)
        value = value.strip("'").strip('"')
        if varname == "DISTRIB_ID":
            yield "vendor", value
        elif varname == "DISTRIB_RELEASE":
            yield "version", value
        elif varname == "DISTRIB_CODENAME":
            yield "code_name", value.title()
        elif varname == "DISTRIB_DESCRIPTION":
            yield "name", value


_DEBIAN_CODE_NAMES: Final = (
    ("2.0.", "Hamm"),
    ("2.1.", "Slink"),
    ("2.2.", "Potato"),
    ("3.0.", "Woody"),
    ("3.1.", "Sarge"),
    ("4.", "Etch"),
    ("5.", "Lenny"),
    ("6.", "Squeeze"),
    ("7.", "Wheezy"),
    ("8.", "Jessie"),
    ("9.", "Stretch"),
    ("10.", "Buster"),
    ("11.", "Bullseye"),
)


# Do not overwrite Ubuntu information
def inv_lnx_parse_debian(line: _Line) -> _KVPairs:
    entry = line[0]
    yield "name", "Debian " + entry
    yield "vendor", "Debian"
    yield "version", entry

    for prefix, code_name in _DEBIAN_CODE_NAMES:
        if entry.startswith(prefix):
            yield "code_name", code_name
            return


def inv_lnx_parse_cma(line: _Line) -> _KVPairs:
    yield "name", "Checkmk Appliance " + line[0]
    yield "vendor", "tribe29 GmbH"
    yield "version", line[0]
    yield "code_name", None


def inv_lnx_parse_gentoo(line: _Line) -> _KVPairs:
    entry = line[0]
    yield "name", entry
    yield "vendor", "Gentoo"
    parts = entry.split(" ")
    yield "version", parts.pop(-1)
    yield "code_name", None


_HANDLERS: Final = (
    ("/usr/share/cma/version", inv_lnx_parse_cma),
    ("/etc/os-release", inv_lnx_parse_os),
    ("/etc/gentoo-release", inv_lnx_parse_gentoo),
    ("/etc/SuSE-release", inv_lnx_parse_suse),
    ("/etc/oracle-release", inv_lnx_parse_oracle_vm_server),
    ("/etc/redhat-release", inv_lnx_parse_redhat),
    ("/etc/lsb-release", inv_lnx_parse_lsb),
    ("/etc/debian_version", inv_lnx_parse_debian),
)

#
#  code from lnx_distro.py end
#


def _get_distro(lnx_distro) -> Dict[str, str]:
    if isinstance(lnx_distro, list):
        lnx_distro = _parse_lnx_distro(lnx_distro)
    for file_name, handler in _HANDLERS:
        if file_name in lnx_distro:
            distro = dict(handler(lnx_distro[file_name]))
            if distro['vendor'].lower() in ['centos', 'red hat']:
                distro['cmk_code'] = f'el{distro["version"]}'
            elif 'suse' in distro['vendor'].lower():
                try:
                    major, minor = distro['version'].split('.')
                    distro['cmk_code'] = f'sles{major}sp{minor}'
                except ValueError:
                    distro['cmk_code'] = f'sles{distro["version"]}'
            elif distro['vendor'].lower() == 'tribe29 gmbh':
                if distro['version'] < '1.5':
                    distro['cmk_code'] = 'cma-2'
                else:
                    distro['cmk_code'] = 'cma-3'

            return distro
    return {}


def _get_dat_from_checkmk(cache_file: str, timeout: int) -> str:
    url = 'https://download.checkmk.com/stable_downloads.json'

    response = requests.get(
        url=url,
        timeout=timeout,
        # verify=not args.no_cert_check,
    )
    if response.status_code == 200:
        page_source = response.text
        with open(cache_file, 'w') as f:
            f.write(page_source)
        return page_source
    else:
        return '{}'


def _get_cmk_update_data(timeout: int) -> Optional[Dict[str, Any]]:
    omd_root = os.environ['OMD_ROOT']
    cache_file = omd_root + '/tmp/check_mk/cache/cmk_downloads'
    # cache_file = omd_root + '/var/check_mk/cmk_downloads'
    # page_source = '{}'

    if os.path.isfile(cache_file):
        now_time = int(time.time())
        modify_time = int(os.path.getmtime(cache_file))
        if (now_time - modify_time) < 86400:
            with open(cache_file, 'r') as f:
                page_source = f.read()
        else:
            page_source = _get_dat_from_checkmk(cache_file, timeout)
    else:
        page_source = _get_dat_from_checkmk(cache_file, timeout)

    try:
        return json.loads(page_source)
    except json.JSONDecodeError:
        return {}


def discovery_checkmk_update(section_lnx_distro, section_omd_info) -> DiscoveryResult:
    if section_omd_info is not None:
        for site in section_omd_info.get('sites', {}).keys():
            yield Service(item=site)


def check_checkmk_update(item, params, section_lnx_distro, section_omd_info) -> CheckResult:
    if not section_lnx_distro:
        yield Result(
            state=State.WARN,
            summary='Operating System data not found. Check if HW/SW inventory is active and the "Operating System" '
                    'data are present in the inventory. (The mk_inventory.linux agent plugin needs to be deployed).'
        )
        return

    try:
        site = section_omd_info.get('sites')[item]
    except KeyError:
        yield Result(state=State.UNKNOWN, summary='Item not found in agent data')
        return

    cmk_update_data = _get_cmk_update_data(params['timeout'])

    distro = _get_distro(section_lnx_distro)
    used_version = site['used_version'].split('.')
    checkmk_version = '.'.join(used_version[:-1])
    cmk_code = distro.get('cmk_code', distro.get('code_name'))
    edition = used_version[-1]

    download_url_base = 'https://download.checkmk.com/checkmk'

    editions = {
        'cre': 'Checkmk Raw Edition',
        'cfe': 'Checkmk Enterprise Free Edition',
        'cee': 'Checkmk Enterprise Standard Edition',
        'cme': 'Checkmk Enterprise Managed Services Edition',
    }

    classes = {
        'stable': {
            'branches': [],
            'latest_branch': '',
            'latest_version': '',
        },
        'oldstable': {
            'branches': [],
            'latest_branch': '',
            'latest_version': '',
        },
        'beta': {
            'branches': [],
            'latest_branch': '',
            'latest_version': '',
        },
        'innovation': {
            'branches': [],
            'latest_branch': '',
            'latest_version': '',
        }
    }

    for branch in cmk_update_data['checkmk'].keys():
        _class = cmk_update_data['checkmk'][branch]['class']
        classes[_class]['branches'].append(branch)
        if classes[_class]['latest_branch']:
            if cmk_update_data['checkmk'][branch]['release_date'] > cmk_update_data['checkmk'][classes[_class]['latest_branch']]['release_date']:
                classes[_class]['latest_branch'] = branch
        else:
            classes[_class]['latest_branch'] = branch

    for _class in classes.keys():
        if classes[_class]['latest_branch']:
            classes[_class]['latest_version'] = cmk_update_data['checkmk'][classes[_class]['latest_branch']]['version']

    latest_stable = classes['stable']['latest_version']
    latest_old_stable = classes['oldstable']['latest_version']

    yield Result(
        state=State.OK,
        summary=f'{edition.upper()} {checkmk_version}, on {distro.get("name")}',
        details=f'{editions.get(edition, edition)} {checkmk_version}, on {distro.get("name")}'
    )
    # yield Result(state=State.OK, notice=f'Edition: {editions.get(edition, edition)}')

    if not re.match(r'\d\d\d\d\.\d\d\.\d\d$', checkmk_version):  # not daily build
        cmk_base_version = checkmk_version[:5]  # works only as long there are only single digit versions
        # get release information from cmk_update_data for cmk base version
        release_info = cmk_update_data['checkmk'].get(cmk_base_version)
        if release_info:
            if release_info['class'] == 'oldstable':
                old_stable = release_info['version']
                if checkmk_version != release_info['version']:
                    yield Result(
                        state=State(params['state_not_latest_base']),
                        notice=f'Update available: {old_stable}'
                    )
                else:
                    yield Result(state=State.OK, notice=f'No update for this release available')
                yield Result(state=State(params['state_not_on_stable']), summary=f'Latest stable: {latest_stable}')
            elif release_info['class'] == 'stable':
                stable = release_info['version']
                if checkmk_version != stable:
                    yield Result(
                        state=State(params['state_not_latest_base']),
                        notice=f'Update available: {stable}'
                    )
                else:
                    yield Result(state=State.OK, notice=f'No update available')
        else:
            yield Result(
                state=State(params['state_on_unsupported']),
                notice=f'Unsupported version {checkmk_version}'
            )
    else:
        yield Result(state=State.OK, summary=f'This is a daily build of CMK')

    cfw_latest = '0.0.0'
    cfw_current_latest = '0.0.0'
    if distro['name'].lower().startswith('checkmk appliance'):
        cfw_current = distro['version']
        cfw_current_main = '.'.join(cfw_current.split('.')[:2])
        for version in cmk_update_data['appliance']:
            if version.startswith(cfw_current_main):
                cfw_current_latest = version
            if version > cfw_latest:
                cfw_latest = version
        if cfw_current_latest == '0.0.0':
            yield Result(
                state=State(params['state_cfw_unsupported']),
                notice=f'Appliance firmware {cfw_current} is unsupported'
            )
        elif cfw_current == cfw_current_latest:
            yield Result(state=State.OK, notice=f'Appliance firmware in line with version {cfw_current_main}')
        else:
            yield Result(
                state=State(params['state_cfw_not_latest_base']),
                notice=f'Appliance firmware update available {cfw_current_latest}'
            )
        message = f'Latest appliance firmware {cfw_latest}'
        if cfw_current_latest < cfw_latest:
            yield Result(state=State(params['state_cfw_not_latest']), notice=message)
        else:
            yield Result(state=State.OK, notice=message)

    # output available releases
    yield Result(
        state=State.OK,
        notice=f'\nAvailable CMK releases:'
    )
    for branch in cmk_update_data['checkmk'].keys():
        latest_version = cmk_update_data['checkmk'][branch]['version']
        release_class = cmk_update_data['checkmk'][branch]["class"]
        release_date = cmk_update_data['checkmk'][branch]["release_date"]
        release_date = time.strftime('%Y-%m-%d', time.strptime(time.ctime(release_date)))

        try:
            file = cmk_update_data['checkmk'][branch]['editions'][edition][cmk_code.lower()][0]
        except KeyError:
            file = None

        if file:
            url = f'{download_url_base}/{latest_version}/{file}'
        else:
            url = f'no download available for your distribution ({cmk_code}).'

        yield Result(
            state=State.OK,
            notice=f'{branch}: '
                   f'Release date: {release_date}, '
                   f'State: {release_class}, '
                   f'Latest version: {latest_version},'
                   f'URL: {url}'
        )

    # add patch level as metric to have a litle release history
    if len(latest_stable) == 5:
        latest_stable += 'p00'  # check for initial release (no patch level)
    yield Metric(value=int(latest_stable.split('p')[-1]), name='latest_stable_patch', boundaries=(0, None))
    yield Metric(value=int(latest_old_stable.split('p')[-1]), name='old_stable_patch', boundaries=(0, None))
    # yield Metric(value=int(appliance.split('.')[-1]), name='appliance_patch', boundaries=(0, None))


register.check_plugin(
    name='checkmk_update',
    service_name='Checkmk Update %s',
    sections=['lnx_distro', 'omd_info'],
    discovery_function=discovery_checkmk_update,
    check_function=check_checkmk_update,
    check_default_parameters={
        'state_on_unsupported': 2,
        'state_not_latest_base': 1,
        'state_not_on_stable': 1,
        'state_cfw_unsupported': 2,
        'state_cfw_not_latest_base': 1,
        'state_cfw_not_latest': 1,
        'state_unknown': 1,
        'timeout': 5,
        # 'no_cert_check': False,
    },
    check_ruleset_name='checkmk_update',
)
