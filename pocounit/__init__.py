# coding=utf-8
from __future__ import print_function

import os
import inspect

from pocounit.case import PocoTestCase
from pocounit.runner import PocoTestRunner
from pocounit.suite import PocoTestSuite

from pocounit.result.collector import PocoResultCollector
from pocounit.result.emitter import PocoTestResultEmitter
from pocounit.result.trace import ScriptTracer
from pocounit.result.record import ScreenRecorder
from pocounit.result.action import ActionRecorder
from pocounit.result.app_runtime import AppRuntimeLog
from pocounit.result.runner_runtime import RunnerRuntimeLog
from pocounit.result.assertion import AssertionRecorder

from airtest.cli.runner import device as current_device

__author__ = 'lxn3032'


def has_override(method, subCls, baseCls):
    return getattr(subCls, method).__func__ is not getattr(baseCls, method).__func__


def main():
    project_root = os.getenv("PROJECT_ROOT") or os.getcwd()
    print('using "{}" as project root.'.format(project_root))

    current_frame = inspect.currentframe()
    caller = current_frame.f_back
    test_case_filename = caller.f_code.co_filename  # 脚本务必是绝对路径才行
    test_case_dir = os.path.dirname(test_case_filename)
    caller_scope = caller.f_locals
    print('this testcase filename is "{}".'.format(test_case_filename))

    # 这部分代码放到loader里
    Cases = [v for k, v in caller_scope.items()
             if type(v) is type
             and v is not PocoTestCase
             and issubclass(v, PocoTestCase)
             and has_override("runTest", v, PocoTestCase)
             ]

    # collect result
    collector = PocoResultCollector(project_root, [test_case_filename], test_case_dir)
    runner_runtime_log = RunnerRuntimeLog(collector)
    tracer = ScriptTracer(collector)
    screen_recorder = ScreenRecorder(collector, current_device())
    action_recorder = ActionRecorder(collector)
    app_runtime_log = AppRuntimeLog(collector)
    assertion_recorder = AssertionRecorder(collector)

    suite = PocoTestSuite()
    for Case in Cases:
        Case.set_testcase_assets_dir(test_case_dir)
        Case.set_result_collector(collector)
        Case.add_result_emitter('runnerRuntimeLog', runner_runtime_log)
        Case.add_result_emitter('tracer', tracer)
        Case.add_result_emitter('screenRecorder', screen_recorder)
        Case.add_result_emitter('actionRecorder', action_recorder)
        Case.add_result_emitter('appRuntimeLog', app_runtime_log)
        Case.add_result_emitter('assertionRecorder', assertion_recorder)
        suite.addTest(Case())

    # launch test
    runner = PocoTestRunner()
    result = runner.run(suite)
    if not result.wasSuccessful():
        exit(-1)
