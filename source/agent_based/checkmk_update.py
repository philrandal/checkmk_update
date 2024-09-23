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
# 2023-03-28: added Checkmk Cloud Edition
# 2023-04-11: added support for the beta release, minor changes in the output
# 2023-05-19: changed metric data form stable/old stable to cmk/cfw main version
# 2023-07-06: changed position of items in detailed output
# 2023-07-07: added support for AlmaLinux and Rocky Linux
# 2023-07-08: added support for ol -> Oracle Linux
# 2023-07-10: added support for rhel -> Red Hat Enterprise Linux. THX to Rickard Eriksson
# 2024-01-01: fixed missing CMK download URL in service details
# 2024-01-01: moved WATO/metrics from ~/local/share/check_mk/web/.. to ~/var/lib/checkmk/gui/.. for CMK 2.2.0
# 2024-04-30: refactoring for CMK 2.3.0 (adjusted to new section_lnx_distro format only)
# 2ß24-05-23: readded code to get cmk_code for ose version
#             added support for Opensuse-Leap

# Known issues -> resolved :-)
# for new Linux distributions (with code name) the plugin needs to be updated :-(, this will be not necessary if tribe
# moves the distro parsing in lnx_distro to the parsing function where it belongs.
# 2023-07-08:
# opened PR610 https://github.com/Checkmk/checkmk/pull/610 --> closed unmerged
# 2023-10-20: Merged/Adjusted by Moritz: https://github.com/Checkmk/checkmk/commit/e0ee2bad5914013cbf7b3c9b5b31a479fa4d2837


# sample lnx_distro section
# # {'name': 'Debian GNU/Linux 12 (bookworm)', 'version': '12', 'code_name': 'Bookworm', 'vendor': 'Debian'}

import re
import json
import time
import os

import requests
from _collections_abc import Mapping
from typing import Dict, Any
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

)


def _get_dat_from_checkmk(cache_file: str, timeout: int) -> str:
    url = 'https://download.checkmk.com/stable_downloads.json'

    # ToDo: add error handling (i.e.: ConnectionError)
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


def _get_cmk_update_data(timeout: int) -> Dict[str, Any] | None:
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


def _get_cmk_code(lnx_distro: Mapping[str, str]) -> str | None:
    if cmk_code := lnx_distro.get('cmk_code', lnx_distro.get('code_name')):
        return cmk_code

    # ol -> Oracle Linux
    if lnx_distro['vendor'].lower() in [
            'centos', 'red hat', 'rhel', 'ol', 'almalinux', 'rocky'
    ]:
        return f'el{lnx_distro["version"].split(".")[0]}'
    elif lnx_distro['vendor'].lower() in ['suse', 'opensuse-leap']:
        try:
            major, minor = lnx_distro['version'].split('.')
        except ValueError:
            return f'sles{lnx_distro["version"]}'
        else:
            return f'sles{major}sp{minor}'
    elif lnx_distro['vendor'].lower() in ['tribe29 gmbh', 'checkmk gmbh']:
        if lnx_distro['version'] < '1.5':
            return 'cma-2'
        else:
            return 'cma-3'


def discovery_checkmk_update(section_lnx_distro, section_omd_info) -> DiscoveryResult:
    if section_omd_info is not None:
        for site in section_omd_info.get('sites', {}).keys():
            yield Service(item=site)


def check_checkmk_update(item, params, section_lnx_distro, section_omd_info) -> CheckResult:
    if not section_lnx_distro:
        yield Result(
            state=State.WARN,
            summary=
            'Operating System data not found. Check if HW/SW inventory is active and the "Operating System" '
            'data are present in the inventory. (The mk_inventory.linux agent plugin needs to be deployed).'
        )
        return

    try:
        site = section_omd_info.get('sites')[item]
    except KeyError:
        yield Result(state=State.UNKNOWN,
                     summary='Item not found in agent data')
        return

    cmk_update_data = _get_cmk_update_data(params['timeout'])

    used_version = site['used_version'].split('.')
    checkmk_version = '.'.join(used_version[:-1])
    cmk_code = _get_cmk_code(section_lnx_distro)
    edition = used_version[-1]

    download_url_base = 'https://download.checkmk.com/checkmk'

    editions = {
        'cre': 'Checkmk Raw Edition',
        'cfe': 'Checkmk Enterprise Free Edition',
        'cee': 'Checkmk Enterprise Standard Edition',
        'cme': 'Checkmk Enterprise Managed Services Edition',
        'cce': 'Checkmk Cloud Edition',
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
            if cmk_update_data['checkmk'][branch][
                    'release_date'] > cmk_update_data['checkmk'][
                        classes[_class]['latest_branch']]['release_date']:
                classes[_class]['latest_branch'] = branch
        else:
            classes[_class]['latest_branch'] = branch

    for _class in classes.keys():
        if classes[_class]['latest_branch']:
            classes[_class]['latest_version'] = cmk_update_data['checkmk'][
                classes[_class]['latest_branch']]['version']

    latest_stable = classes['stable']['latest_version']
    # latest_old_stable = classes['oldstable']['latest_version']

    yield Result(state=State.OK,
                 summary=f'{edition.upper()} {checkmk_version}',
                 details=f'{editions.get(edition, edition)} {checkmk_version}')
    yield Result(state=State.OK,
                 summary=f'OS: {section_lnx_distro.get("name")}')

    if not re.match(r'\d\d\d\d\.\d\d\.\d\d$',
                    checkmk_version):  # not daily build
        cmk_base_version = checkmk_version[:
                                           5]  # works only as long there are only single digit versions
        # get release information from cmk_update_data for cmk base version
        release_info = cmk_update_data['checkmk'].get(cmk_base_version)
        yield Result(state=State.OK,
                     summary=f'Branch: {release_info["class"]}')
        if release_info:
            if checkmk_version != release_info['version']:
                yield Result(
                    state=State(params['state_not_latest_base']),
                    notice=f'Update available: {release_info["version"]}')
            else:
                yield Result(state=State.OK,
                             notice=f'No update for this release available')
            if release_info['class'] != 'stable':
                yield Result(state=State(params['state_not_on_stable']),
                             summary=f'Latest stable: {latest_stable}')
        else:
            yield Result(state=State(params['state_on_unsupported']),
                         notice=f'Unsupported version {checkmk_version}')
    else:
        yield Result(state=State.OK, summary=f'This is a daily build of CMK')

    cfw_latest = '0.0.0'
    cfw_current_latest = '0.0.0'
    if section_lnx_distro['name'].lower().startswith('checkmk appliance'):
        cfw_current = section_lnx_distro['version']
        cfw_current_main = '.'.join(cfw_current.split('.')[:2])
        for version in cmk_update_data['appliance']:
            # add a litle appliance patch history
            yield Metric(value=int(version.split('.')[-1]),
                         name=f'appliance_{"_".join(version.split(".")[:2])}',
                         boundaries=(0, None))
            if version.startswith(cfw_current_main):
                cfw_current_latest = version
            if version > cfw_latest:
                cfw_latest = version
        if cfw_current_latest == '0.0.0':
            yield Result(
                state=State(params['state_cfw_unsupported']),
                notice=f'Appliance firmware {cfw_current} is unsupported')
        elif cfw_current == cfw_current_latest:
            yield Result(
                state=State.OK,
                notice=
                f'Appliance firmware in line with version {cfw_current_main}')
        else:
            yield Result(
                state=State(params['state_cfw_not_latest_base']),
                notice=
                f'Appliance firmware update available {cfw_current_latest}')
        message = f'Latest appliance firmware {cfw_latest}'
        if cfw_current_latest < cfw_latest:
            yield Result(state=State(params['state_cfw_not_latest']),
                         notice=message)
        else:
            yield Result(state=State.OK, notice=message)

    # output available releases
    yield Result(state=State.OK, notice='\nAvailable CMK releases:')
    for branch in cmk_update_data['checkmk'].keys():
        latest_version = cmk_update_data['checkmk'][branch]['version']
        release_class = cmk_update_data['checkmk'][branch]["class"]
        release_date = cmk_update_data['checkmk'][branch]["release_date"]
        release_date = time.strftime('%Y-%m-%d',
                                     time.strptime(time.ctime(release_date)))

        try:
            file = cmk_update_data['checkmk'][branch]['editions'][edition][
                cmk_code.lower()][0]
        except (KeyError, AttributeError):
            file = None

        if file:
            url = f'{download_url_base}/{latest_version}/{file}'
        else:
            _message = 'no download available for your edition/distribution/branch'
            url = f'{_message} ({edition.upper()}/{cmk_code}/{release_class}).'

        yield Result(state=State.OK,
                     notice=f'{branch}: '
                     f'Latest version: {latest_version}, '
                     f'Release date: {release_date}, '
                     f'Branch: {release_class}, '
                     f'URL: {url}')
        # add a little patch history
        yield Metric(value=int(
            latest_version.split('p')[-1].split('b')[-1].split('i')[-1].split(
                '.')[-1]),
                     name=f'cmk_branch_{branch.replace(".", "_")}',
                     boundaries=(0, None))


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
