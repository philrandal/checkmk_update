#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# License: GNU General Public License v2
#
# Author: thl-cmk[at]outlook[dot]com
# URL   : https://thl-cmk.hopto.org
# Date  : 2026-03-14
# File  : ~/local/lib/python3/cmk_addons/plugins/checkmk_update/lib/lib_global.py



from ast import parse as ast_parse, Assign as ast_Assign
from pathlib import Path
from cmk.utils.paths import check_mk_config_dir

def get_global_http_proxies():
    cmk_globals_ast = ast_parse(Path(f'{check_mk_config_dir}/wato/global.mk').read_text())
    cmk_globals_ast.body = [
        node for node in cmk_globals_ast.body if
        isinstance(node, ast_Assign) and node.targets[0].id == 'http_proxies'
    ]
    http_proxies: dict = {}
    exec(compile(cmk_globals_ast, '<ast>', 'exec'), {}, http_proxies)
    return http_proxies