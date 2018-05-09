# coding=utf-8
from __future__ import print_function

import os
import inspect

from pocounit.case import PocoTestCase
from pocounit.runner import PocoTestRunner
from pocounit.suite import PocoTestSuite

from pocounit.utils.misc import has_override


def run(suite):
    if isinstance(suite, PocoTestCase):
        case = suite
        suite = PocoTestSuite()
        suite.addTest(case)
    runner = PocoTestRunner()
    return runner.run(suite)


def main():
    # testcase detection
    current_frame = inspect.currentframe()
    caller = current_frame.f_back
    test_case_filename = os.path.abspath(caller.f_code.co_filename)  # 脚本务必是绝对路径才行
    caller_scope = caller.f_locals
    print('this testcase filename is "{}".'.format(test_case_filename))

    # 这部分代码放到loader里
    Cases = [v for k, v in caller_scope.items()
             if type(v) is type
             and v is not PocoTestCase
             and issubclass(v, PocoTestCase)
             and has_override("runTest", v, PocoTestCase)
             ]

    suite = PocoTestSuite()
    for Case in Cases:
        case = Case()
        suite.addTest(case)

    runner = PocoTestRunner()
    result = runner.run(suite)

    if not result.wasSuccessful():
        exit(-1)

