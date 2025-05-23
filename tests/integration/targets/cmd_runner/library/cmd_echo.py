#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2022, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import traceback


DOCUMENTATION = ""

EXAMPLES = ""

RETURN = ""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.community.general.plugins.module_utils.cmd_runner import CmdRunner, cmd_runner_fmt as fmt


def main():
    module = AnsibleModule(
        argument_spec=dict(
            cmd=dict(type="str", default="echo"),
            path_prefix=dict(type="str"),
            arg_formats=dict(type="dict", default={}),
            arg_order=dict(type="raw", required=True),
            arg_values=dict(type="dict", default={}),
            check_mode_skip=dict(type="bool", default=False),
            aa=dict(type="raw"),
            tt=dict(),
        ),
        supports_check_mode=True,
    )
    p = module.params

    info = None

    arg_formats = {}
    for arg, fmt_spec in p['arg_formats'].items():
        func = getattr(fmt, fmt_spec['func'])
        args = fmt_spec.get("args", [])

        arg_formats[arg] = func(*args)

    try:
        runner = CmdRunner(module, [module.params["cmd"], '--'], arg_formats=arg_formats, path_prefix=module.params["path_prefix"])

        with runner.context(p['arg_order'], check_mode_skip=p['check_mode_skip']) as ctx:
            result = ctx.run(**p['arg_values'])
            info = ctx.run_info
        check = "check"
        rc, out, err = result if result is not None else (None, None, None)

        module.exit_json(rc=rc, out=out, err=err, info=info)
    except Exception as exc:
        module.fail_json(rc=1, module_stderr=traceback.format_exc(), msg="Module crashed with exception")


if __name__ == '__main__':
    main()
