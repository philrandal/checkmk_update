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
# 2025-12-19: added cache_time option on a which from Checkmk
#             added proxy option

from typing import Final

from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    Integer,
    ServiceState,
    TimeMagnitude,
    TimeSpan,
    validators,
    Proxy,
    ProxySchema,
)
from cmk.rulesets.v1.form_specs.validators import Message, ValidationError
from cmk.rulesets.v1.rule_specs import (
    CheckParameters,
    Help,
    HostAndItemCondition,
    Title,
    Topic,
)


class ValidateDictNotEmpty:
    def __init__(self, strict: bool = False, option_name: str | None = None) -> None:
        if option_name is None:
            self.error_msg = Message('Select at least one option')
        else:
            self.error_msg = Message(f'Select at least one option under {option_name}')

        self.strict: Final[bool] = strict

    def __call__(self, value: str) -> None:
        if len(value) == 0:
            raise ValidationError(self.error_msg)


def migrate_to_connection_settings(value: object) -> object:
    if not isinstance(value, dict):  # unknown format
        return value
    if not (keys := value.keys()):  # not configured
        return value
    if 'connection_settings' in keys or 'update_states' in keys:  # already migrated
        return value

    migrated_value = {}
    if 'timeout' in keys:
        migrated_value['connection_settings'] = {'timeout': value.pop('timeout')}

    for key, value_ in value.items():
        if not 'update_states' in migrated_value.keys():
            migrated_value['update_states'] = {}
            migrated_value['update_states'][key] = value_
    return migrated_value


def parameter_form_checkmk_update():
    return Dictionary(
        title=Title('Settings of Check MK Update check'),
        migrate=migrate_to_connection_settings,
        custom_validate=[ValidateDictNotEmpty()],
        elements={
            'connection_settings': DictElement(
                parameter_form=Dictionary(
                    title=Title('Connection settings for "download.checkmk.com"'),
                    custom_validate=[
                        ValidateDictNotEmpty(option_name='Connection settings for "download.checkmk.com"')
                    ],
                    elements={
                        'cache_time': DictElement(
                            parameter_form=TimeSpan(
                                title=Title('Cacheing time'),
                                prefill=DefaultValue(86400),  # one day
                                displayed_magnitudes=[TimeMagnitude.DAY, TimeMagnitude.HOUR],
                                help_text=Help(
                                    'The time the check will cache the update data. Default is one day.'
                                ))),
                        'timeout': DictElement(
                            parameter_form=Integer(
                                title=Title('Connection Timeout for update data download'),
                                prefill=DefaultValue(5),
                                unit_symbol='seconds',
                                custom_validate=[validators.NumberInRange(min_value=1, max_value=10)],
                                help_text=Help(
                                    'The connection timeout in seconds for accessing the update data. Default is 5 seconds'
                                ))),
                        'proxy': DictElement(
                            parameter_form=Proxy(
                                title=Title('HTTP proxy (global configured proxy does not work right now'),
                                allowed_schemas=frozenset([ProxySchema.HTTP])
                            )),
                    })),
            'update_states': DictElement(
                parameter_form=Dictionary(
                    title=Title('Update states'),
                    custom_validate=[ValidateDictNotEmpty(option_name='Update states')],
                    elements={
                        'state_on_unsupported': DictElement(
                            parameter_form=ServiceState(
                                title=Title('State if CMK base version is older than old stable base version.'),
                                prefill=DefaultValue(ServiceState.CRIT),
                            )),
                        'state_not_latest_base': DictElement(
                            parameter_form=ServiceState(
                                title=Title('State if CMK version is older than latest version of base version.'),
                                prefill=DefaultValue(ServiceState.WARN),
                            )),
                        'state_not_on_stable': DictElement(
                            parameter_form=ServiceState(
                                title=Title('State if CMK version is an old stable release.'),
                                prefill=DefaultValue(ServiceState.WARN),
                            )),
                        'state_unknown': DictElement(
                            parameter_form=ServiceState(
                                title=Title('State if CMK base version could not be detected.'),
                                prefill=DefaultValue(ServiceState.WARN),
                            )),
                        'state_cfw_unsupported': DictElement(
                            parameter_form=ServiceState(
                                title=Title('State if CMK appliance firmware is unsupported.'),
                                prefill=DefaultValue(ServiceState.WARN),
                            )),
                        'state_cfw_not_latest_base': DictElement(
                            parameter_form=ServiceState(
                                title=Title('State if CMK appliance firmware update is available (same base version).'),
                                prefill=DefaultValue(ServiceState.WARN),
                            )),
                        'state_cfw_not_latest': DictElement(
                            parameter_form=ServiceState(
                                title=Title('State if CMK appliance firmware is not the latest release.'),
                                prefill=DefaultValue(ServiceState.WARN),
                            )),
                    })),
        })


rule_spec_checkmk_update = CheckParameters(
    name='checkmk_update',
    title=Title('Checkmk Update'),
    topic=Topic.APPLICATIONS,
    parameter_form=parameter_form_checkmk_update,
    condition=HostAndItemCondition(item_title=Title('Checkmk Update Instance')),
)
