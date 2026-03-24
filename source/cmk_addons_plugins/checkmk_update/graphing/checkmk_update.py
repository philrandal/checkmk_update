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
# 2025-05-29: rewritten vor graphing APIv1 by timo[dot]lechleiter[at]web[dot]de)

from cmk.graphing.v1.metrics import Metric, Color, Unit, DecimalNotation
from cmk.graphing.v1.graphs import Graph, MinimalRange
from cmk.graphing.v1 import Title

UNIT_NUMBER = Unit(DecimalNotation(''))

# Metrics

metric_cmk_installed_patch_level= Metric(
    name='installed_patch_level',
    title=Title('Installed patch level'),
    unit=UNIT_NUMBER,
    color=Color.GRAY,
)
metric_cmk_branch_1_6_0 = Metric(
    name='cmk_branch_1_6_0',
    title=Title('CMK 1.6.0'),
    unit=UNIT_NUMBER,
    color=Color.LIGHT_BLUE,
)
metric_cmk_branch_2_0_0 = Metric(
    name='cmk_branch_2_0_0',
    title=Title('CMK 2.0.0'),
    unit=UNIT_NUMBER,
    color=Color.BLUE,
)
metric_cmk_branch_2_1_0 = Metric(
    name='cmk_branch_2_1_0',
    title=Title('CMK 2.1.0'),
    unit=UNIT_NUMBER,
    color=Color.PINK,
)
metric_cmk_branch_2_2_0 = Metric(
    name='cmk_branch_2_2_0',
    title=Title('CMK 2.2.0'),
    unit=UNIT_NUMBER,
    color=Color.GREEN,
)
metric_cmk_branch_2_3_0 = Metric(
    name='cmk_branch_2_3_0',
    title=Title('CMK 2.3.0'),
    unit=UNIT_NUMBER,
    color=Color.ORANGE,
)
metric_cmk_branch_2_4_0 = Metric(
    name='cmk_branch_2_4_0',
    title=Title('CMK 2.4.0'),
    unit=UNIT_NUMBER,
    color=Color.PURPLE,
)
metric_cmk_branch_2_5_0 = Metric(
    name='cmk_branch_2_5_0',
    title=Title('CMK 2.5.0'),
    unit=UNIT_NUMBER,
    color=Color.DARK_YELLOW,
)
metric_appliance_1_5 = Metric(
    name='appliance_1_5',
    title=Title('CFW 1.5'),
    unit=UNIT_NUMBER,
    color=Color.BLUE,
)
metric_appliance_1_6 = Metric(
    name='appliance_1_6',
    title=Title('CFW 1.6'),
    unit=UNIT_NUMBER,
    color=Color.GREEN,
)
metric_appliance_1_7 = Metric(
    name='appliance_1_7',
    title=Title('CFW 1.7'),
    unit=UNIT_NUMBER,
    color=Color.ORANGE,
)
metric_appliance_1_8 = Metric(
    name='appliance_1_8',
    title=Title('CFW 1.8'),
    unit=UNIT_NUMBER,
    color=Color.PURPLE,
)
# Graphs
graph_checkmk_update_cmk = Graph(
    name='checkmk_update_cmk',
    title=Title('CheckMK patch level release history'),
    simple_lines=[
        'cmk_branch_1_6_0',
        'cmk_branch_2_0_0',
        'cmk_branch_2_1_0',
        'cmk_branch_2_2_0',
        'cmk_branch_2_3_0',
        'cmk_branch_2_4_0',
        'cmk_branch_2_5_0',
    ],
    compound_lines=[
        'installed_patch_level'
    ],
    optional=[
        'cmk_branch_1_6_0',
        'cmk_branch_2_0_0',
        'cmk_branch_2_1_0',
        'cmk_branch_2_2_0',
        'cmk_branch_2_3_0',
        'cmk_branch_2_4_0',
        'cmk_branch_2_5_0',
        'installed_patch_level',
    ],

    minimal_range=MinimalRange(0, 60),
)
graph_checkmk_update_cfw = Graph(
    name='checkmk_update_cfw',
    title=Title('CheckMK firmware patch level release history'),
    simple_lines=[
        'appliance_1_5',
        'appliance_1_6',
        'appliance_1_7',
        'appliance_1_8',
    ],
    optional=[
        'appliance_1_5',
        'appliance_1_6',
        'appliance_1_7',
        'appliance_1_8',
    ],
    minimal_range=MinimalRange(0, 20),
)
