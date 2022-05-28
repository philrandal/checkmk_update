#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#


from cmk.gui.i18n import _
from cmk.gui.plugins.wato import (
    HostRulespec,
    rulespec_registry,
)
from cmk.gui.plugins.wato.utils import PasswordFromStore
from cmk.gui.valuespec import (
    Dictionary,
    FixedValue,
    Integer,
    TextAscii,
    Tuple,
    DropdownChoice,
)

from cmk.gui.plugins.wato.datasource_programs import (
    RulespecGroupDatasourceProgramsOS,
)


def _valuespec_special_agents_checkmk_update():
    return Dictionary(
        elements=[
            ('no-cert-check',
             FixedValue(
                 True,
                 title=_('Disable SSL certificate validation'),
                 totext=_('SSL certificate validation is disabled'),
             )),
            ('timeout',
             Integer(
                 title=_('Connect Timeout'),
                 help=_('The network timeout in seconds'),
                 default_value=60,
                 minvalue=1,
                 unit=_('seconds'),
             )),
        ],
        title=_('Checkmk update'),
    )


rulespec_registry.register(
    HostRulespec(
        group=RulespecGroupDatasourceProgramsOS,
        name='special_agents:checkmk_update',
        valuespec=_valuespec_special_agents_checkmk_update,
    ))
