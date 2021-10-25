#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# License: GNU General Public License v2
#
# Author: thl-cmk[at]outlook[dot]com
# URL   : https://thl-cmk.hopto.org
# Date  : 2021-10-25
#
# Check_MK checkmk_updates WATO plugin
#
#
#

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
    MonitoringState,
)

from cmk.gui.plugins.wato import (
    CheckParameterRulespecWithItem,
    rulespec_registry,
    RulespecGroupCheckParametersOperatingSystem,
)


def _parameter_valuespec_checkmk_update():
    return Dictionary(elements=[
        ('state_on_unsupported',
         MonitoringState(
             default_value=2,
             title=_('State if CMK base version older than old stable base version.'),
         )),
        ('state_not_latest_base',
         MonitoringState(
             default_value=1,
             title=_('State if version is older than latest version of base version.'),
         )),
        ('state_unknown',
         MonitoringState(
             default_value=1,
             title=_('State if CMK base version could not be detected.'),
         )),
    ])


rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name='checkmk_update',
        group=RulespecGroupCheckParametersOperatingSystem,
        match_type='dict',
        parameter_valuespec=_parameter_valuespec_checkmk_update,
        title=lambda: _('Checkmk update'),
    ))
