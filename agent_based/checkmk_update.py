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
# 2021-10-26: minor fixes (removed unused prints)
# 2021-11-04: fixed missing "versions" key in "release" section
# 2021-11-17: added checkmk appliance version
# 2021-12-07: added metrics for patch release history (a little fun) maybe one day of (cache, only checks once a day)

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
    Metric,
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
        if release not in ['latestStable']:  # , 'virt'
            if agentoutput[release].get('versions'):
                for version in agentoutput[release]['versions'].keys():
                    if version not in ['master daily']:
                        status = agentoutput[release]['versions'][version]['class']
                        if release == 'virt':
                            status = 'virt'
                        versions[status] = version
    return versions


def discovery_checkmk_update(section: List) -> DiscoveryResult:
    yield Service()


def check_checkmk_update(params, section) -> CheckResult:
    # {'latestStable': '2.0.0p17', 'stable': '2.0.0p17', 'oldstable': '1.6.0p27', 'virt': '1.4.17'}

    versions = get_general_version_infos()
    checkmk_version = versions['version']
    platform = versions['os'].split(' ')[0]
    os = ' '.join(versions['os'].split(' ')[1:])
    old_stable = section["oldstable"]
    stable = section['stable']
    latest_stable = section['latestStable']
    appliance = section['virt']

    yield Result(state=State.OK, summary=f'Checkmk version: {checkmk_version}, on {platform} {os}')

    if not re.match(r'\d\d\d\d\.\d\d\.\d\d$', checkmk_version):
        cmk_base_version = '.'.join(checkmk_version.split('.')[:2])
        old_base_version = '.'.join(old_stable.split('.')[:2])
        stable_base = '.'.join(stable.split('.')[:2])

        if float(cmk_base_version) < float(old_base_version):
            yield Result(
                state=State(params['state_on_unsupported']),
                notice=f'You are using an old version, Upgrade at least to old stable {old_base_version}'
            )
        elif cmk_base_version == old_base_version:
            if checkmk_version != old_stable:
                yield Result(
                    state=State(params['state_not_latest_base']),
                    notice=f'Update available, old stable: {old_stable}'
                )
            else:
                yield Result(
                    state=State.OK,
                    summary=f'In line with old stable, You wight upgrade to latest sable: {latest_stable}'
                )
        elif cmk_base_version == stable_base:
            if checkmk_version != stable:
                yield Result(
                    state=State(params['state_not_latest_base']),
                    notice=f'Update available, stable: {stable}'
                )
            else:
                yield Result(state=State.OK, summary=f'In line with stable')
        else:
            yield Result(state=State(params['state_unknown']), notice=f'Could not detect yor base version of Checkmk')

    if latest_stable != stable:
        yield Result(state=State.OK, notice=f'Latest stable: {latest_stable}')
    yield Result(state=State.OK, notice=f'Stable: {stable}')
    yield Result(state=State.OK, notice=f'Old stable: {old_stable}')
    yield Result(state=State.OK, notice=f'Checkmk Appliance: {appliance}')

    # add patch level as metric to have a litle release history
    if latest_stable != stable:
        yield Metric(value=int(latest_stable.split('p')[-1]), name='latest_stable_patch',)
    yield Metric(value=int(stable.split('p')[-1]), name='stable_patch',)
    yield Metric(value=int(old_stable.split('p')[-1]), name='old_stable_patch',)


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
