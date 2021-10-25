#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.
"""
Agent CheckMK Download
Write checkmk_download_ sections containing JSON formatted results from https://checkmk.com/download URL
"""

#
# Author: thl-cmk[at]outlook[dot]com
# URL   : https://thl-cmk.hopto.org
# Date  : 2021-10-20
#
# CheckMK special agent for checkmk.com/download
#

#
# sample crul
#


import sys
import argparse
import logging
import json
from typing import Optional, Sequence
from time import asctime
import requests

from cmk.special_agents.utils import vcrtrace


def parse_arguments(argv: Sequence[str]) -> argparse.Namespace:
    """'
    Parse arguments needed to construct an URL and for connection conditions
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', required=True, help='Host to query')
    parser.add_argument('--timeout', '-t', type=float, default=60, help='API call timeout in seconds', )
    parser.add_argument('--verbose', '-v', action='count', default=0)
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> None:

    def setup_logging(verbose: bool) -> None:
        logging.basicConfig(level={
            0: logging.WARN,
            1: logging.INFO,
            2: logging.DEBUG
        }.get(verbose, logging.DEBUG), )
        # urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # type: ignore
        logging.getLogger('urllib3.connectionpool').setLevel(logging.INFO)
        logging.getLogger('vcr').setLevel(logging.WARN)

    if argv is None:
        argv = sys.argv[1:]

    args = parse_arguments(argv)
    setup_logging(args.verbose)
    logging.debug('cmd: argv=%r, turned into: %r', argv, args.__dict__)

    url = 'https://checkmk.com/download'

    response = requests.get(
        url=url,
        # auth=HTTPBasicAuth(args.username, args.password),
        timeout=args.timeout,
        # verify=not args.no_cert_check,
        # headers=headers,
    )
    if response.status_code == 200:
        downloads = response.text
        downloads = downloads[downloads.find(':downloads=') + 12:downloads.find("'", downloads.find(':downloads=') + 12)]
        print('<<<inv_checkmk_downloads:sep(0)>>>\n')
        print(downloads)
        print('<<<checkmk_update:sep(0)>>>\n')
        print(downloads)


if __name__ == '__main__':
    main()
