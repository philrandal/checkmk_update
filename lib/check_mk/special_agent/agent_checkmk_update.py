#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.
"""
Agent CheckMK Update
Write JSON formatted results from https://download.checkmk.com/stable_downloads.json
"""

#
# Author: thl-cmk[at]outlook[dot]com
# URL   : https://thl-cmk.hopto.org
# Date  : 2021-10-20
#
# CheckMK special agent for checkmk update state
#
# 2022-05-27: modified for new download page
#


import sys
import argparse
import logging
from typing import Optional, Sequence
import requests
import os
import time


def parse_arguments(argv: Sequence[str]) -> argparse.Namespace:
    """'
    Parse arguments needed to construct an URL and for connection conditions
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='Host to query')
    parser.add_argument('--timeout', '-t', type=float, default=60, help='API call timeout in seconds', )
    parser.add_argument('--verbose', '-v', action='count', default=0)
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> None:
    agent_version = 'v.0.3'
    agent_build = '2022-05-27'
    agent_os = 'Linux'

    def setup_logging(verbose: bool) -> None:
        logging.basicConfig(level={
            0: logging.WARN,
            1: logging.INFO,
            2: logging.DEBUG
        }.get(verbose, logging.DEBUG), )
        # urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # type: ignore
        logging.getLogger('urllib3.connectionpool').setLevel(logging.INFO)
        logging.getLogger('vcr').setLevel(logging.WARN)

    def get_dat_from_checkmk():
        response = requests.get(
            url=url,
            timeout=args.timeout,
            # verify=not args.no_cert_check,
        )
        if response.status_code == 200:
            page_source = response.text
            with open(cache_file, 'w') as f:
                f.write(page_source)
            return page_source

    if argv is None:
        argv = sys.argv[1:]

    args = parse_arguments(argv)
    setup_logging(args.verbose)
    logging.debug('cmd: argv=%r, turned into: %r', argv, args.__dict__)
    omd_root = os.environ['OMD_ROOT']
    cache_file = omd_root + '/tmp/check_mk/cache/cmk_downloads'
    url = 'https://download.checkmk.com/stable_downloads.json'

    if os.path.isfile(cache_file):
        now_time = int(time.time())
        modify_time = int(os.path.getmtime(cache_file))
        if (now_time - modify_time) < 86400:
            with open(cache_file, 'r') as f:
                page_source = f.read()
        else:
            page_source = get_dat_from_checkmk()
    else:
        page_source = get_dat_from_checkmk()

    # print('<<<inv_checkmk_update:sep(0)>>>\n')
    # print(page_source)
    print('<<<checkmk_update:sep(0)>>>\n')
    print(page_source)
    print('<<<check_mk>>>')
    print(f'Version: {agent_version}')
    print(f'AgentOS: {agent_os}')
    print(f'BuildDate: {agent_build}')
    print(f'Hostname: {args.host}')
    print(f'Architecture: 64bit')


if __name__ == '__main__':
    main()
