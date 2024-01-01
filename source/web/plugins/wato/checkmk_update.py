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
# 2022-11-30: fixed CheckParameterRulespecWithoutItem (from CheckParameterRulespecWithItem)
# 2023-03-14: merged with agent_checkmk_update WATO rules
# 2023-03-19: added CMK appliance options

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
    MonitoringState,
    FixedValue,
    Integer,
)

from cmk.gui.plugins.wato.utils import (
    CheckParameterRulespecWithoutItem,
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
             title=_(
                 'State if CMK version is older than latest version of base version.'),
         )),
        ('state_not_on_stable',
         MonitoringState(
             default_value=1,
             title=_(
                 'State if CMK version is an old stable release.'),
         )),
        ('state_unknown',
         MonitoringState(
             default_value=1,
             title=_('State if CMK base version could not be detected.'),
         )),
        ('state_cfw_unsupported',
         MonitoringState(
             default_value=2,
             title=_('State if CMK appliance firmware is unsupported.'),
         )),
        ('state_cfw_not_latest_base',
         MonitoringState(
             default_value=1,
             title=_('State if CMK appliance firmware update available (same base version).'),
         )),
        ('state_cfw_not_latest',
         MonitoringState(
             default_value=1,
             title=_('State if CMK appliance firmware is not the latest release.'),
         )),
        # ('no_cert_check',
        #     FixedValue(
        #         True,
        #         title=_('Disable SSL certificate validation'),
        #         totext=_(''),
        #         help=_('Dont check the TLS certificate for https://download.checkmk-com')
        #     )),
        ('timeout',
            Integer(
                title=_('Connection Timeout for update data download'),
                help=_('The connection timeout in seconds for accessing '
                       'https://download.checkmk-com/stable_downloads.json. Default is 5 seconds'),
                default_value=5,
                minvalue=1,
                unit=_('seconds'),
            )),
    ])


rulespec_registry.register(
    CheckParameterRulespecWithoutItem(
        check_group_name='checkmk_update',
        group=RulespecGroupCheckParametersOperatingSystem,
        match_type='dict',
        parameter_valuespec=_parameter_valuespec_checkmk_update,
        title=lambda: _('Checkmk update'),
    ))
