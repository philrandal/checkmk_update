#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# License: GNU General Public License v2
#
# Author: thl-cmk[at]outlook[dot]com
# URL   : https://thl-cmk.hopto.org
# Date  : 2021-10-21
#
# Inventory of Checkmk downloads
#
# 2021-11-17: added checkmk appliance downloads

# sample agent output
#
#
import json
from typing import List
from cmk.base.plugins.agent_based.agent_based_api.v1 import (
    register,
    TableRow,
)

from cmk.base.plugins.agent_based.agent_based_api.v1.type_defs import (
    InventoryResult,
)


def parse_inv_checkmk_downloads(string_table) -> List:
    agentoutput = json.loads(string_table[0][0])
    nodes = []
    for relesae in agentoutput.keys():
        if relesae not in ['latestStable']:  # , 'virt'
            product = agentoutput[relesae]['label']
            for version in agentoutput[relesae]['versions'].keys():
                status = agentoutput[relesae]['versions'][version]['class']
                dir_name = agentoutput[relesae]['versions'][version]['dirname']
                for distro in agentoutput[relesae]['versions'][version]['distros'].keys():
                    if distro not in ['docker', 'src', 'changelog']:
                        if relesae != 'virt':
                            for distro_version in agentoutput[relesae]['versions'][version]['distros'][distro]:
                                name = agentoutput[relesae]['versions'][version]['distros'][distro][distro_version]['name']
                                hash = agentoutput[relesae]['versions'][version]['distros'][distro][distro_version]['hash']
                                nodes.append({
                                    'product': product,
                                    'version': version,
                                    'platform': distro,
                                    'os_version': distro_version,
                                    'status': status,
                                    'name': name,
                                    'hash': hash,
                                    'url': f'https://download.checkmk.com/checkmk/{dir_name}/{name}'
                                })
                        else:
                            name = agentoutput[relesae]['versions'][version]['distros'][distro]['name']
                            hash = agentoutput[relesae]['versions'][version]['distros'][distro]['hash']
                            nodes.append({
                                    'product': product,
                                    'version': version,
                                    'platform': distro,
                                    'os_version': 'N/A',
                                    'status': status,
                                    'name': name,
                                    'hash': hash,
                                    'url': f'https://download.checkmk.com/checkmk/{dir_name}/{name}'
                                })
                    elif distro not in ['changelog']:
                        name = agentoutput[relesae]['versions'][version]['distros'][distro]['name']
                        hash = agentoutput[relesae]['versions'][version]['distros'][distro]['hash']
                        nodes.append({
                            'product': product,
                            'version': version,
                            'platform': distro,
                            'os_version': 'N/A',
                            'status': status,
                            'name': name,
                            'hash': hash,
                            'url': f'https://download.checkmk.com/checkmk/{dir_name}/{name}'
                        })
    return nodes


def inventory_inv_checkmk_downloads(section: List) -> InventoryResult:
    path = ['software', 'checkmk', 'downloads']

    for node in section:
        yield TableRow(
            path=path,
            key_columns={
                'product': node['product'],
                'version': node['version'],
                'platform': node['platform'],
                'os_version': node['os_version'],
            },
            inventory_columns={
                'status': node['status'],
                'file': node['name'],
                'hash': node['hash'],
                'url': node['url']
            },
        )


register.agent_section(
    name='inv_checkmk_downloads',
    parse_function=parse_inv_checkmk_downloads,
)

register.inventory_plugin(
    name='inv_checkmk_downloads',
    sections=['inv_checkmk_downloads'],
    inventory_function=inventory_inv_checkmk_downloads,
)
