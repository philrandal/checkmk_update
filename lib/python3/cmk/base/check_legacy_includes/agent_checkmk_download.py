#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


import json


def parse_checkmk_download(key, info):
    elements = json.loads(info[0][0])['queryResponse']['entity']
    return {
        item['@id']: item  #
        for elem in elements  #
        for item in (elem[key],)
    }
