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
#                     "impish": [
#                         "check-mk-managed-2.1.0_0.impish_amd64.deb",
#                         "e16313c22655c7b73605718884a4d857b889db442cc54875ff97c2e322d74d30"
#                     ],
#                     "jammy": [
#                         "check-mk-managed-2.1.0_0.jammy_amd64.deb",
#                         "b61aa84efc8ee8d99d00e3c9b786460f293c35f425acf237213496f7d28d412d"
#                     ],
#                     "stretch": [
#                         "check-mk-managed-2.1.0_0.stretch_amd64.deb",
#                         "6c5fab5db4de942185a191a29261531fc291df7906f88afda7d1ab608c09c090"
#                     ],
#                     "xenial": [
#                         "check-mk-managed-2.1.0_0.xenial_amd64.deb",
#                         "6c57c6e723b3f7a516d0874cd405866908edbd443fc4fe45c04431d22514ee03"
#                     ],
#                     "cma-3": [
#                         "check-mk-managed-2.1.0-3-x86_64.cma",
#                         "bc05572179302ef798eea2f80aca6d6c84a453afcf3ba9daeb14b3bae1ed5243"
#                     ],
#                     "el7": [
#                         "check-mk-managed-2.1.0-el7-38.x86_64.rpm",
#                         "a8fa2f6dc2d401ed9c65ef765034d71214eafbc6dee3d7a3c03985d16337b8f8"
#                     ],
#                     "el8": [
#                         "check-mk-managed-2.1.0-el8-38.x86_64.rpm",
#                         "3821eb16e31a4aecfc31a09488e7c3c3f9097adf55c29efa0fd5bab742e431be"
#                     ],
#                     "sles12sp3": [
#                         "check-mk-managed-2.1.0-sles12sp3-38.x86_64.rpm",
#                         "10394df58b42d0eb823b722482f938071a5198ee6caa8a6cda12d1fd240d15d2"
#                     ],
#                     "sles12sp4": [
#                         "check-mk-managed-2.1.0-sles12sp4-38.x86_64.rpm",
#                         "3d598bdb9e58f39a81b8aea9c2d507c4ae0fe382dce9bc8db134ddbfc1d58d3c"
#                     ],
#                     "sles12sp5": [
#                         "check-mk-managed-2.1.0-sles12sp5-38.x86_64.rpm",
#                         "6b97e835e9b9cad6805d472fddcbade360b9d69104111766dcb4ff50f0f0afa7"
#                     ],
#                     "sles15": [
#                         "check-mk-managed-2.1.0-sles15-38.x86_64.rpm",
#                         "1a8bf238a10766a051233b5978f5c347449266f64bbb4e0a00d590f9620bf9f6"
#                     ],
#                     "sles15sp1": [
#                         "check-mk-managed-2.1.0-sles15sp1-38.x86_64.rpm",
#                         "e801b7904dacef57c7cfe729c10e28a067bcaaf46730952fb5e2c3db8134f5e6"
#                     ],
#                     "sles15sp2": [
#                         "check-mk-managed-2.1.0-sles15sp2-38.x86_64.rpm",
#                         "5a98ac4124a943785fc2b1753f16614b0ad316b2cdcefae87a525ece94f80af2"
#                     ],
#                     "sles15sp3": [
#                         "check-mk-managed-2.1.0-sles15sp3-38.x86_64.rpm",
#                         "7b41935ca0468dfc4217ab836d4a0b7ad982b846a5be24041ecb282ef3d131bb"
#                     ],
#                     "bionic": [
#                         "check-mk-managed-2.1.0_0.bionic_amd64.deb",
#                         "618ddeb474bfc6ba8c1883aa88a375793c1edf71e9c51895605f4f8f2aa30c0d"
#                     ],
#                     "bullseye": [
#                         "check-mk-managed-2.1.0_0.bullseye_amd64.deb",
#                         "2003fc551b3317efbfc45d53ebd78807c07a72d90bffa9489c81ce78b5cd7e3b"
#                     ],
#                     "buster": [
#                         "check-mk-managed-2.1.0_0.buster_amd64.deb",
#                         "aa36433ee7e5ca25d5e25604c151685a7eaa5b3d99437aad468e20c1c964a331"
#                     ],
#                     "focal": [
#                         "check-mk-managed-2.1.0_0.focal_amd64.deb",
#                         "352e28e459fe3f1129c6d59f544b4a0a036e89a0449ead682d6960405e44e937"
#                     ],
#                     "cma-2": [
#                         "check-mk-managed-2.1.0-2-x86_64.cma",
#                         "e5c53df1aab71b7a1b1472543e509ca71b8192a1af83856b0d2612f121ea3a47"
#                     ],
#                     "docker": [
#                         "check-mk-managed-docker-2.1.0.tar.gz"
#                     ]
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
from typing import List, Dict, Any
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
    try:
        agentoutput = json.loads(string_table[0][0])
    except json.JSONDecodeError:
        return
    return agentoutput


def discovery_checkmk_update(section: List) -> DiscoveryResult:
    yield Service()


def _get_distro_code():
    omd_root = os.environ['OMD_ROOT']
    distro_info_file = omd_root + '/share/omd/distro.info'
    distro_code = None
    if os.path.isfile(distro_info_file):
        with open(distro_info_file, 'r') as f:
            distro_info = f.read()
        distro_info = distro_info.split('\n')
        for line in distro_info:
            if line.startswith('DISTRO_CODE'):
                distro_code = line.split('=')[1].strip(' ')
                break
    return distro_code


def check_checkmk_update(params, section: Dict[str, Any]) -> CheckResult:

    versions = get_general_version_infos()
    checkmk_version = versions['version']
    platform = versions['os'].split(' ')[0]
    os = ' '.join(versions['os'].split(' ')[1:])
    edition = versions['edition']
    distro_code = _get_distro_code()
    download_url_base = 'https://download.checkmk.com/checkmk'

    # get versions
    stable_versions = []
    old_stable_versions = []
    latest_stable_branch = None
    latest_old_stable_branch = None
    for branch in section['checkmk'].keys():
        if section['checkmk'][branch]['class'] == 'stable':
            stable_versions += [section['checkmk'][branch]['version']]
            # find latest stable branch by release date
            if latest_stable_branch:
                if section['checkmk'][branch]['release_date'] < section['checkmk'][latest_stable_branch]['release_date']:
                    latest_stable_branch = branch
            else:
                latest_stable_branch = branch

        if section['checkmk'][branch]['class'] == 'oldstable':
            old_stable_versions += [section['checkmk'][branch]['version']]
            # find latest old stable branch by release date
            if latest_old_stable_branch:
                if section['checkmk'][branch]['release_date'] < section['checkmk'][latest_old_stable_branch]['release_date']:
                    latest_old_stable_branch = branch
            else:
                latest_old_stable_branch = branch

    latest_stable = section['checkmk'][latest_stable_branch]['version']
    latest_old_stable = section['checkmk'][latest_old_stable_branch]['version']

    yield Result(state=State.OK, summary=f'CMK: {checkmk_version}, on {platform} {os}, Edition: {edition}')

    if not re.match(r'\d\d\d\d\.\d\d\.\d\d$', checkmk_version):  # not daily build
        cmk_base_version = checkmk_version[:5]  # works only as long there are only single digit versions
        # get release information from section for cmk base version
        release_info = section['checkmk'].get(cmk_base_version)
        if release_info:
            if release_info['class'] == 'oldstable':
                old_stable = release_info['version']
                if checkmk_version != release_info['version']:
                    yield Result(
                        state=State(params['state_not_latest_base']),
                        notice=f'Update available, old stable: {old_stable}'
                    )
                else:
                    yield Result(state=State.OK, summary=f'In line with old stable')
                yield Result(state=State.OK, summary=f'You might upgrade to latest stable: {latest_stable}')
            elif release_info['class'] == 'stable':
                stable = release_info['version']
                if checkmk_version != stable:
                    yield Result(
                        state=State(params['state_not_latest_base']),
                        notice=f'Update available, stable: {stable}'
                    )
                else:
                    yield Result(state=State.OK, summary=f'In line with stable')
        else:
            yield Result(
                state=State(params['state_on_unsupported']),
                notice=f'You are using an old (unsupported) version, please upgrade to a supported version'
            )
    else:
        yield Result(state=State.OK, summary=f'This is a daily build of CMK')

    # output available releases
    yield Result(
        state=State.OK,
        notice=f'\nAvailable CMK releases:'
    )
    for branch in section['checkmk'].keys():
        latest_version = section['checkmk'][branch]['version']
        release_class = section['checkmk'][branch]["class"]
        release_date = section['checkmk'][branch]["release_date"]
        release_date = time.strftime('%Y-%m-%d', time.strptime(time.ctime(release_date)))
        file = section['checkmk'][branch]['editions'][edition][distro_code][0]
        yield Result(
            state=State.OK,
            notice=f'{branch}: '
                   f'Release date: {release_date}, '
                   f'State: {release_class}, '
                   f'Latest version: {latest_version},'
                   f'URL: {download_url_base}/{latest_version}/{file}'
        )

    # add patch level as metric to have a litle release history
    if len(latest_stable) == 5:
        latest_stable += 'p00'  # check for initial release (no patch level
    yield Metric(value=int(latest_stable.split('p')[-1]), name='latest_stable_patch', boundaries=(0, None))
    yield Metric(value=int(latest_old_stable.split('p')[-1]), name='old_stable_patch', boundaries=(0, None))
    # yield Metric(value=int(appliance.split('.')[-1]), name='appliance_patch', boundaries=(0, None))


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
