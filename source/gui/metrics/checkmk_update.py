#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# License: GNU General Public License v2
#
# Author: thl-cmk[at]outlook[dot]com
# URL   : https://thl-cmk.hopto.org
# Date  : 2021-12-07
#
# 2024-01-01: moved WATO/metrics from ~/local/share/check_mk/web/.. to ~/var/lib/checkmk/gui/.. for CMK 2.2.0
#             metrics prepared for CMK 2.3.0

from cmk.gui.i18n import _

from cmk.gui.plugins.metrics.utils import (
    check_metrics,
    metric_info,
    graph_info,
)

check_metrics['check_mk-checkmk_update'] = {
    'cmk_branch_1_6_0': {'auto_graph': False},
    'cmk_branch_2_0_0': {'auto_graph': False},
    'cmk_branch_2_1_0': {'auto_graph': False},
    'cmk_branch_2_2_0': {'auto_graph': False},
    'cmk_branch_2_3_0': {'auto_graph': False},
    'appliance_1_5': {'auto_graph': False},
    'appliance_1_6': {'auto_graph': False},
    # old metrics removed at 2023-05-19
    'latest_stable_patch': {'auto_graph': False},
    'old_stable_patch': {'auto_graph': False},
    'stable_patch': {'auto_graph': False},
    'appliance_patch': {'auto_graph': False},
}

metric_info['cmk_branch_1_6_0'] = {'title': _('CMK 1.6.0'), 'unit': 'count', 'color': '11/a', }
metric_info['cmk_branch_2_0_0'] = {'title': _('CMK 2.0.0'), 'unit': 'count', 'color': '21/a', }
metric_info['cmk_branch_2_1_0'] = {'title': _('CMK 2.1.0'), 'unit': 'count', 'color': '31/a', }
metric_info['cmk_branch_2_2_0'] = {'title': _('CMK 2.2.0'), 'unit': 'count', 'color': '26/a', }
metric_info['cmk_branch_2_3_0'] = {'title': _('CMK 2.3.0'), 'unit': 'count', 'color': '41/a', }

metric_info['appliance_1_5'] = {'title': _('CFW 1.5'), 'unit': 'count', 'color': '12/b', }
metric_info['appliance_1_6'] = {'title': _('CFW 1.6'), 'unit': 'count', 'color': '22/b', }

graph_info['checkmk_update_cmk'] = {
    'title': _('CheckMK patch level release history'),
    'metrics': [
        ('cmk_branch_1_6_0', 'line'),
        ('cmk_branch_2_0_0', 'line'),
        ('cmk_branch_2_1_0', 'line'),
        ('cmk_branch_2_2_0', 'line'),
        ('cmk_branch_2_3_0', 'line'),
    ],
    'optional_metrics': [
        'cmk_branch_1_6_0',
        'cmk_branch_2_0_0'
        'cmk_branch_2_1_0',
        'cmk_branch_2_2_0',
        'cmk_branch_2_3_0',
    ],
    'range': (0, 50),
}

graph_info['checkmk_update_cfw'] = {
    'title': _('CheckMK firmware patch level release history'),
    'metrics': [
        ('appliance_1_5', 'line'),
        ('appliance_1_6', 'line'),
    ],
    'optional_metrics': [
        'appliance_1_5',
        'appliance_1_6'
    ],
    'range': (0, 20),
}

