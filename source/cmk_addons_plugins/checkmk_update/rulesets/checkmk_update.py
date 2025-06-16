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
# 2024-01-01: moved WATO/metrics from ~/local/share/check_mk/web/.. to ~/var/lib/checkmk/gui/.. for CMK 2.2.0
# 2025-05-29: rewritten vor ruleset APIv1 by timo[dot]lechleiter[at]web[dot]de)

from cmk.rulesets.v1.form_specs import DefaultValue, Dictionary, DictElement, Integer, ServiceState, validators
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic, Title, Help

def _parameter_valuespec_checkmk_update():
    return Dictionary(
        title=Title('Settings of Check MK Update check'),
        elements={
            'state_on_unsupported': DictElement(
                parameter_form=ServiceState(
                    title=Title('State if CMK base version older than old stable base version.'),
                    prefill=DefaultValue(ServiceState.CRIT),
                ),
            ),
            'state_not_latest_base': DictElement(
                parameter_form=ServiceState(
                    title=Title('State if CMK version is older than latest version of base version.'),
                    prefill=DefaultValue(ServiceState.WARN),
                ),
            ),
            'state_not_on_stable': DictElement(
                parameter_form=ServiceState(
                    title=Title('State if CMK version is an old stable release.'),
                    prefill=DefaultValue(ServiceState.WARN),
                ),
            ),
            'state_unknown': DictElement(
                parameter_form=ServiceState(
                    title=Title('State if CMK base version could not be detected.'),
                    prefill=DefaultValue(ServiceState.WARN),
                ),
            ),
            'state_cfw_unsupported': DictElement(
                parameter_form=ServiceState(
                    title=Title('State if CMK appliance firmware is unsupported.'),
                    prefill=DefaultValue(ServiceState.WARN),
                ),
            ),
            'state_cfw_not_latest_base': DictElement(
                parameter_form=ServiceState(
                    title=Title('State if CMK appliance firmware update available (same base version).'),
                    prefill=DefaultValue(ServiceState.WARN),
                ),
            ),
            'state_cfw_not_latest': DictElement(
                parameter_form=ServiceState(
                    title=Title('State if CMK appliance firmware is not the latest release.'),
                    prefill=DefaultValue(ServiceState.WARN),
                ),
            ),
             'timeout': DictElement(
                parameter_form=Integer(
                    title=Title('Connection Timeout for update data download'),
                    help_text=Help('The connection timeout in seconds for accessing '
                                   'https://download.checkmk-com/stable_downloads.json. Default is 5 seconds'
                    ),
                    prefill=DefaultValue(5),
                    custom_validate=(
                        validators.NumberInRange(min_value=1, max_value=10),
                    ),
                ),
            ),
        },
    )

rule_spec_checkmk_update = CheckParameters(
    name='checkmk_update',
    title=Title('Checkmk Update'),
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_valuespec_checkmk_update,
    condition=HostAndItemCondition(item_title=Title('Checkmk Update Instance')),
)
