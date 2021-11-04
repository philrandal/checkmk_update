#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# License: GNU General Public License v2
#
# Author: thl-cmk[at]outlook[dot]com
# URL   : https://thl-cmk.hopto.org
# Date  : 2021-20-25
#
# Checkmk update status
#
# 2021-11-04: fixed missing "versions" key in "release" section

# sample agent output
#
#
import re
import json
from typing import List
from cmk.base.plugins.agent_based.agent_based_api.v1 import (
    register,
    Result,
    State,
    Service,
)

from cmk.base.plugins.agent_based.agent_based_api.v1.type_defs import (
    DiscoveryResult,
    CheckResult,
)

from cmk.utils.version import get_general_version_infos


def parse_checkmk_update(string_table):
    versions = {}
    agentoutput = json.loads(string_table[0][0])
    versions['latestStable'] = agentoutput['latestStable']
    for release in agentoutput.keys():
        if release not in ['latestStable', 'virt']:
            if agentoutput[release].get('versions'):
                for version in agentoutput[release]['versions'].keys():
                    status = agentoutput[release]['versions'][version]['class']
                    versions[status] = version
    return versions


def discovery_checkmk_update(section: List) -> DiscoveryResult:
    yield Service()


def check_checkmk_update(params, section) -> CheckResult:
    # {'latestStable': '2.0.0p12', 'stable': '2.0.0p12', 'oldstable': '1.6.0p27', 'development': 'master daily'}

    versions = get_general_version_infos()
    checkmk_version = versions['version']
    platform = versions['os'].split(' ')[0]
    os = ' '.join(versions['os'].split(' ')[1:])
    daily_master = False
    olstable = section["oldstable"]
    stable = section['stable']
    latestStable = section["latestStable"]

    yield Result(state=State.OK, summary=f'Your Checkmk version: {checkmk_version}, on {platform} {os}')
    if re.match(r'\d\d\d\d\.\d\d\.\d\d$', checkmk_version):
        daily_master = True
    else:
        cmk_base_version = '.'.join(checkmk_version.split('.')[:2])
        old_base_version = '.'.join(olstable.split('.')[:2])
        stable_base = '.'.join(stable.split('.')[:2])

        if float(cmk_base_version) < float(old_base_version):
            yield Result(state=State(params['state_on_unsupported']), notice=f'You are using an old version, Upgrade at least to old stable {old_base_version}')
        elif cmk_base_version == old_base_version:
            if checkmk_version != olstable:
                yield Result(state=State(params['state_not_latest_base']), notice=f'There is an update for your version available, old stable: {olstable}')
            else:
                yield Result(state=State.OK, summary=f'In line with old stable, You wight upgrade to latest sable: {latestStable}')
        elif cmk_base_version == stable_base:
            if checkmk_version != stable:
                yield Result(state=State(params['state_not_latest_base']), notice=f'There is an update for your version available, stable: {stable}')
            else:
                yield Result(state=State.OK, summary=f'In line with stable')
        else:
            yield Result(state=State(params['state_unknown']), notice=f'Could not detect yor base version of Checkmk')

    if latestStable != stable:
        yield Result(state=State.OK, notice=f'Latest stable: {latestStable}')
    yield Result(state=State.OK, notice=f'Stable: {stable}')
    yield Result(state=State.OK, notice=f'Old stable: {olstable}')


register.agent_section(
    name='checkmk_update',
    parse_function=parse_checkmk_update,
)

register.check_plugin(
    name='checkmk_update',
    service_name='Checkmk Update',
    discovery_function=discovery_checkmk_update,
    check_function=check_checkmk_update,
    check_default_parameters={
        'state_on_unsupported': 2,
        'state_not_latest_base': 1,
        'state_unknown': 1,
    },
    check_ruleset_name='checkmk_update',
)