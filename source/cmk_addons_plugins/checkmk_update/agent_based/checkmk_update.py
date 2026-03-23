#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# License: GNU General Public License v2
#
# Author: thl-cmk[at]outlook[dot]com
# URL   : https://thl-cmk.hopto.org
# Date  : 2021-12-25
# File  : ~/local/lib/python3/cmk_addons/plugins/checkmk_update/agent_based/checkmk_update.py

# Checkmk update status

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
# 2025-05-29: rewritten vor check APIv2 by timo[dot]lechleiter[at]web[dot]de)
# 2025-12-20: added cache_time option on a which from Checkmk
#             added proxy, installed_patch_level
# 2026-03-03: fixed crash on daily build version numbers (wrong regex) (ThX to @gulaschcowboy)
# 2026-03-ß8: added support for global proxies (CMK 2.3/2.4/2.5)
# 2026-03-14: added support for global proxies
# 2026-03-22: fixed crash if version not found in update json

# ######################################################################################################################
# Known issues -> resolved :-)
# for new Linux distributions (with code name) the plugin needs to be updated :-(, this will be not necessary if tribe
# moves the distro parsing in lnx_distro to the parsing function where it belongs.
# 2023-07-08: opened PR610 https://github.com/Checkmk/checkmk/pull/610 --> closed unmerged
# 2023-10-20: Merged/Adjusted by Moritz: https://github.com/Checkmk/checkmk/commit/e0ee2bad5914013cbf7b3c9b5b31a479fa4d2837
# ######################################################################################################################

# sample lnx_distro section
# {'name': 'Debian GNU/Linux 12 (bookworm)', 'version': '12', 'code_name': 'Bookworm', 'vendor': 'Debian'}

import json
import os
import re
import time
import requests

from collections.abc import Mapping
from pydantic import BaseModel
from typing import Literal

from cmk.agent_based.v2 import (
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Metric,
    Result,
    Service,
    State,
)

from cmk.utils.paths import tmp_dir

from cmk_addons.plugins.checkmk_update.lib.lib_global import get_global_http_proxies

# no_host_name_import = False
# try:
#     from cmk.base.check_api import host_name
# except ImportError:
#     no_host_name_import = True


PROXY = tuple[
    Literal['cmk_postprocessed'],
    Literal['environment_proxy', 'no_proxy', 'stored_proxy', 'explicit_proxy'],
    str,
]


class ConnectionSettings(BaseModel):
    cache_time: int | None = 86400
    timeout: int | None = 5
    proxy: PROXY | None = None


class UpdateStates(BaseModel):
    state_cfw_not_latest: int | None = 1
    state_cfw_not_latest_base: int | None = 1
    state_cfw_unsupported: int | None = 2
    state_not_latest_base: int | None = 1
    state_not_on_stable: int | None = 1
    state_on_unsupported: int | None = 2
    state_unknown: int | None = 1


class Params(BaseModel):
    connection_settings: ConnectionSettings | None = ConnectionSettings()
    update_states: UpdateStates | None = UpdateStates()
    # host_name: str | None


# from rule_set in agent_based check
# {'proxy': ('cmk_postprocessed', 'no_proxy', '')},
# {'proxy': ('cmk_postprocessed', 'environment_proxy', '')},
# {'proxy': ('cmk_postprocessed', 'stored_proxy', 'vsquid')},
# {'proxy': ('cmk_postprocessed', 'explicit_proxy', 'http://squid:8080/')},
# in server_side_calls
# 'proxy': NoProxy(type='no_proxy')
# 'proxy': EnvProxy(type='env_proxy')
# 'proxy': URLProxy(type='url_proxy', url='http://vsquid.home.intern:3128')
# 'proxy': URLProxy(type='url_proxy', url='http://explicit.proxy8080')


def _get_dat_from_checkmk(
        cache_file: str,
        timeout: int,
        params_proxy: PROXY | None,
) -> str:
    url = 'https://download.checkmk.com/stable_downloads.json'

    match params_proxy:
        case ("cmk_postprocessed", "stored_proxy", str()):
            http_proxies = get_global_http_proxies()
            if proxy_url := http_proxies.get(params_proxy[2], {}).get('proxy_url'):  # cmk 2.3/2.4 'proxy_url': 'http://your.proxy.server:3128'
                proxies = {'https': proxy_url, 'http': proxy_url}
            elif proxy_config := http_proxies.get(params_proxy[2], {}).get('proxy_config'):  # cmk 2.5 'proxy_config': {'port': 3128, 'proxy_server_name': 'your.proxy.server', 'scheme': 'http'}
                proxy_url = f'{proxy_config["scheme"]}://{proxy_config["proxy_server_name"]}:{proxy_config["port"]}'
                proxies = {'https': proxy_url, 'http': proxy_url}
            else:
                proxies = {}
        case ("cmk_postprocessed", "environment_proxy", str()):
            proxies = {}
        case ("cmk_postprocessed", "explicit_proxy", str()):
            proxies = {'https': params_proxy[2], 'http': params_proxy[2]}
        case ("cmk_postprocessed", "no_proxy", str()):
            proxies = {'https': '', 'http': ''}
        case _:
            proxies = {}

    # ToDo: add error handling (i.e.: ConnectionError)
    response = requests.get(
        url=url,
        timeout=timeout,
        proxies=proxies,
    )
    if response.status_code == 200:
        page_source = response.text
        with open(cache_file, 'w', encoding='utf-8') as cachefile:
            cachefile.write(page_source)
        return page_source

    return '{}'


def _get_cmk_update_data(
        timeout: int,
        cache_time: int,
        proxy: PROXY | None,
) -> dict[str, object] | None:
    cache_file = os.path.join(tmp_dir, 'cache/cmk_downloads.json')
    # cache_file = omd_root + '/var/check_mk/cmk_downloads'
    # page_source = '{}'

    if os.path.isfile(cache_file):
        now_time = int(time.time())
        modify_time = int(os.path.getmtime(cache_file))
        if (now_time - modify_time) < cache_time:
            with open(cache_file, 'r', encoding='utf-8') as cachefile:
                page_source = cachefile.read()
        else:
            page_source = _get_dat_from_checkmk(cache_file, timeout, proxy)
    else:
        page_source = _get_dat_from_checkmk(cache_file, timeout, proxy)

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
        lnx_distro['cmk_code'] = f'el{lnx_distro["version"].split(".")[0]}'
        return lnx_distro['cmk_code']

    if lnx_distro['vendor'].lower() in ['suse', 'opensuse-leap']:
        try:
            major, minor = lnx_distro['version'].split('.')
        except ValueError:
            return f'sles{lnx_distro["version"]}'

        return f'sles{major}sp{minor}'

    if lnx_distro['vendor'].lower() in ['tribe29 gmbh', 'checkmk gmbh']:
        if lnx_distro['version'] < '1.5':
            return 'cma-2'

        return 'cma-3'

    return None


def _get_patch_level(cmk_version: str) -> int:
    return int(cmk_version.split('.')[-1].split('b')[-1].split('i')[-1].split('p')[-1])


def discovery_checkmk_update(section_lnx_distro, section_omd_info, section_ps) -> DiscoveryResult:
    if section_omd_info is not None:
        for site in section_omd_info.get('sites', {}).keys():
            yield Service(item=site)


def check_checkmk_update(item: str, params, section_lnx_distro, section_omd_info, section_ps) -> CheckResult:
    params: Params = Params.model_validate(params)

    docker = False
    if section_ps:
        for process, details in section_ps[1]:
            if '/docker-entrypoint.sh' in details:
                docker = True
                break

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
        yield Result(
            state=State.UNKNOWN,
            summary='Item not found in agent data',
        )
        return

    cmk_update_data = _get_cmk_update_data(
        timeout=params.connection_settings.timeout,
        cache_time=params.connection_settings.cache_time,
        proxy=params.connection_settings.proxy,
    )

    used_version = site['used_version'].split('.')
    checkmk_version = '.'.join(used_version[:-1])
    installed_patch_level = _get_patch_level(checkmk_version)
    edition = used_version[-1]

    if not docker:
        cmk_code = _get_cmk_code(section_lnx_distro)
    else:
        cmk_code = 'docker'

    download_url_base = 'https://download.checkmk.com/checkmk'

    editions = {
        'cre': 'Checkmk Raw Edition',
        'cfe': 'Checkmk Enterprise Free Edition',
        'cee': 'Checkmk Enterprise Standard Edition',
        'cme': 'Checkmk Enterprise Managed Services Edition',
        'cce': 'Checkmk Cloud Edition',
        # cmk 2.5 and up (names are also changed with cmk 2.3.0p45 and 2.4.0p24)
        'community': 'Checkmk Community',
        'pro': 'Checkmk Pro',
        'ultimate': 'Checkmk Ultimate',
        'ultimatemt': 'Checkmk Ultimate with Multi - Tenancy',
        'cloud': 'Checkmk Cloud',
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

    for _class in classes.values():
        if _class['latest_branch']:
            _class['latest_version'] = cmk_update_data['checkmk'][
                _class['latest_branch']]['version']

    latest_stable = classes['stable']['latest_version']
    # latest_old_stable = classes['oldstable']['latest_version']

    yield Result(
        state=State.OK,
        summary=f'{edition.upper()} {checkmk_version}',
        details=f'{editions.get(edition, edition)} {checkmk_version}',
    )

    if not docker:
        yield Result(
            state=State.OK,
            summary=f'OS: {section_lnx_distro.get("name")}',
        )
    else:
        yield Result(
            state=State.OK,
            summary=f'OS: {section_lnx_distro.get("name")} on Docker',
        )

    yield Metric(
        name='installed_patch_level',
        value=installed_patch_level,
        boundaries=(0, None),
    )

    if re.match(r'\d\.\d\.\d-\d\d\d\d\.\d\d\.\d\d$', checkmk_version):  # not daily build (i.e. "2.5.0-2026.03.04")
        yield Result(state=State.OK, summary='This is a daily build of CMK')
    else:
        cmk_base_version = checkmk_version[:5] # works only as long as there are only single digit versions
        # get release information from cmk_update_data for cmk base version
        release_info = cmk_update_data['checkmk'].get(cmk_base_version)
        if release_info:
            yield Result(
                state=State.OK,
                summary=f'Branch: {release_info["class"]}',
            )
            if checkmk_version != release_info['version']:
                yield Result(
                    state=State(params.update_states.state_not_latest_base),
                    notice=f'Update available: {release_info["version"]}',
                )
            else:
                yield Result(
                    state=State.OK,
                    notice='No update for this release available',
                )
            if release_info['class'] != 'stable':
                yield Result(
                    state=State(params.update_states.state_not_on_stable),
                    summary=f'Latest stable: {latest_stable}',
                )
        else:
            yield Result(
                state=State(params.update_states.state_on_unsupported),
                notice=f'Version {checkmk_version} not supported/not found in update info',
            )

    cfw_latest = '0.0.0'
    cfw_current_latest = '0.0.0'
    if section_lnx_distro['name'].lower().startswith('checkmk appliance'):
        cfw_current = section_lnx_distro['version']
        cfw_current_main = '.'.join(cfw_current.split('.')[:2])
        for version in cmk_update_data['appliance']:
            # add a little appliance patch history
            yield Metric(
                value=int(version.split('.')[-1]),
                name=f'appliance_{"_".join(version.split(".")[:2])}',
                boundaries=(0, None),
            )
            if version.startswith(cfw_current_main):
                cfw_current_latest = version
            if version > cfw_latest:
                cfw_latest = version
        if cfw_current_latest == '0.0.0':
            yield Result(
                state=State(params.update_states.state_cfw_unsupported),
                notice=f'Appliance firmware {cfw_current} is unsupported',
            )
        elif cfw_current == cfw_current_latest:
            yield Result(
                state=State.OK,
                notice=f'Appliance firmware in line with version {cfw_current_main}',
            )
        else:
            yield Result(
                state=State(params.update_states.state_cfw_not_latest_base),
                notice=f'Appliance firmware update available {cfw_current_latest}',
            )
        message = f'Latest appliance firmware {cfw_latest}'
        if cfw_current_latest < cfw_latest:
            yield Result(
                state=State(params.update_states.state_cfw_not_latest),
                notice=message,
            )
        else:
            yield Result(state=State.OK, notice=message)

    # output available releases
    yield Result(state=State.OK, notice='\nAvailable CMK releases:')
    for branch in cmk_update_data['checkmk'].keys():
        latest_version = cmk_update_data['checkmk'][branch]['version']
        release_class = cmk_update_data['checkmk'][branch]["class"]
        release_date = cmk_update_data['checkmk'][branch]["release_date"]
        release_date = time.strftime('%Y-%m-%d', time.strptime(time.ctime(release_date)))

        # add a little patch history
        yield Metric(
            value=_get_patch_level(latest_version),
            name=f'cmk_branch_{branch.replace(".", "_")}',
            boundaries=(0, None),
        )

        try:
            file = cmk_update_data['checkmk'][branch]['editions'][edition][
                cmk_code.lower()][0]
        except (KeyError, AttributeError):
            file = None

        if file:
            url = f'{download_url_base}/{latest_version}/{file}'
        else:
            if params.get('skip_no_download_url'):
                continue
            _message = 'no download available for your edition/distribution/branch'
            url = f'{_message} ({edition.upper()}/{cmk_code}/{release_class}).'

        yield Result(
            state=State.OK,
            notice=f'{branch}: '
                   f'Latest version: {latest_version}, '
                   f'Release date: {release_date}, '
                   f'Branch: {release_class}, '
                   f'URL: {url}',
        )



check_plugin_checkmk_update = CheckPlugin(
    name='checkmk_update',
    service_name='Checkmk Update %s',
    sections=['lnx_distro', 'omd_info', 'ps'],
    discovery_function=discovery_checkmk_update,
    check_function=check_checkmk_update,
    check_default_parameters={
        # # Don't try this hack at home, we (the Checkmk Dev team) are trained professionals.
        # # This next entry will be postprocessed by the backend and return the Checkmk host object name.
        # # This is not official and can vanish with every Checkmk update :-(
        # 'host_name': ('cmk_postprocessed', 'host_name', None),
    },
    check_ruleset_name='checkmk_update',
)
