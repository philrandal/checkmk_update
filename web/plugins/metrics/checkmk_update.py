#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# License: GNU General Public License v2
#
# Author: thl-cmk[at]outlook[dot]com
# URL   : https://thl-cmk.hopto.org
# Date  : 2021-12-07
#
#
#

from cmk.gui.i18n import _

from cmk.gui.plugins.metrics import (
    metric_info,
    graph_info,
    perfometer_info
)

metric_info['latest_stable_patch'] = {
    'title': _('Latest stable'),
    'unit': 'count',
    'color': '11/a',
}

metric_info['old_stable_patch'] = {
    'title': _('Old stable'),
    'unit': 'count',
    'color': '31/a',
}

metric_info['stable_patch'] = {
    'title': _('Stable'),
    'unit': 'count',
    'color': '41/a',
}
metric_info['appliance_patch'] = {
    'title': _('Appliance'),
    'unit': 'count',
    'color': '11/b',
}

graph_info['checkmk_update_patch_level'] = {
    'title': _('CheckMK patch level release history'),
    'metrics': [
        ('appliance_patch', '-area'),
        ('latest_stable_patch', '-area'),
        ('old_stable_patch', 'area'),
    ],
    'optional_metrics': [
        'latest_stable_patch',
        'old_stable_patch'
        'appliance_patch',
    ],
    'range': (0, 50),
}

# perfometer_info.append(('stacked', [
#     {
#         'type': 'linear',
#         'segments': ['stable_patch'],
#         'total': 50,
#     },
#     {
#         'type': 'linear',
#         'segments': ['old_stable_patch'],
#         'total': 50,
#     }
# ]))
