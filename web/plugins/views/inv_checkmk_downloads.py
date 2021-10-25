#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# License: GNU General Public License v2
#
# Author: thl-cmk[at]outlook[dot]com
# URL   : https://thl-cmk.hopto.org
# Date  : 2021-10-20
#
# CheckMK views for Checkmk downloads
#


import time

from cmk.gui.plugins.views.inventory import (
    declare_invtable_view,
    decorate_inv_paint,
)

from cmk.gui.plugins.visuals.inventory import (
    FilterInvtableText,
)

from cmk.gui.i18n import _

from cmk.gui.plugins.views import (
    inventory_displayhints,
)
from cmk.gui.htmllib import HTML


inventory_displayhints.update({
    '.software.checkmk.downloads:': {
        'title': _('Checkmk downloads'),
        'keyorder':
            [
                'product', 'version', 'platform', 'os_version', 'status', 'file'
            ],
        'view': 'invcheckmkdownload_of_host',
    },
    '.software.checkmk.downloads:*.product': {'title': _('Product'), },
    '.software.checkmk.downloads:*.version': {'title': _('Release'), },
    '.software.checkmk.downloads:*.platform': {'title': _('Platform'), },
    '.software.checkmk.downloads:*.os_version': {'title': _('OS Version'), },
    '.software.checkmk.downloads:*.status': {'title': _('Status'), },
    '.software.checkmk.downloads:*.file': {'title': _('File'), },
    '.software.checkmk.downloads:*.hash': {'title': _('File hash (SHA256)'), },
    '.software.checkmk.downloads:*.url': {'title': _('Download URL'), },
})

declare_invtable_view('invcheckmkdownload', '.software.checkmk.downloads:', _('Checkmk downloads'), _('Checkmk downloads'))
