# coding=utf-8

import inspect
import os
import sys
import traceback
import unittest
import warnings

from unittest.util import safe_repr

from pocounit.assets_manager import AssetsManager
from pocounit.result import PocoTestResult
from pocounit.result.collector import PocoResultCollector
from pocounit.result.trace import ScriptTracer
from pocounit.result.record import ScreenRecorder
from pocounit.result.action import ActionRecorder
from pocounit.result.app_runtime import AppRuntimeLog
from pocounit.result.runner_runtime import RunnerRuntimeLog
from pocounit.result.assertion import AssertionRecorder

from pocounit.utils.misc import get_project_root


class PocoTestCase(unittest.TestCase):
    """
    * longMessage: determines whether long messages (including repr of
        objects used in assert methods) will be printed on failure in *addition*
        to any explicit message passed.
    """
    longMessage = True

    _resule_collector = None
    _result_emitters = {}  # name -> PocoTestResultEmitter
    _addons = []
    _assets_manager = None

    def __init__(self):
        super(PocoTestCase, self).__init__()
        test_case_filename = os.path.abspath(inspect.getfile(self.__class__))
        test_case_dir = os.path.dirname(test_case_filename)
        project_root = get_project_root(test_case_filename)
        print('using "{}" as project root.'.format(project_root))
        self.__class__._assets_manager = AssetsManager(project_root)

        collector = PocoResultCollector(project_root, [test_case_filename], self.name(), test_case_dir)
        runner_runtime_log = RunnerRuntimeLog(collector)
        tracer = ScriptTracer(collector)
        screen_recorder = ScreenRecorder(collector)
        action_recorder = ActionRecorder(collector)
        app_runtime_log = AppRuntimeLog(collector)
        assertion_recorder = AssertionRecorder(collector)

        self.set_result_collector(collector)
        self.add_result_emitter('runnerRuntimeLog', runner_runtime_log)
        self.add_result_emitter('tracer', tracer)
        self.add_result_emitter('screenRecorder', screen_recorder)
        self.add_result_emitter('actionRecorder', action_recorder)
        self.add_result_emitter('appRuntimeLog', app_runtime_log)
        self.add_result_emitter('assertionRecorder', assertion_recorder)

    @classmethod
    def name(cls):
        """
        改写此方法来自定义testcase的名字，允许中文，请使用utf-8编码的str或者unicode

        :return:
        """

        if type(cls) is type:
            return cls.__name__
        else:
            return cls.__class__.__name__

    @classmethod
    def setUpClass(cls):
        """
        用例预处理，加载自定义插件等

        :return: 
        """
        pass

    def setUp(self):
        """
        初始化一个testcase
        不要把测试逻辑放到这里写，setUp报错的话也相当于整个case报错

        """

        pass

    def runTest(self):
        """
        testcase的正文，把要执行的测试和包括断言语句都写到这里

        """

        raise NotImplementedError

    def tearDown(self):
        """
        一个testcase的清场工作

        """

        pass

    @classmethod
    def tearDownClass(cls):
        """
        用例后处理

        :return: 
        """
        pass

    def shortDescription(self):
        """
        描述这个testcase的细节，如果需要的话就override这个方法
        
        :return: <str>
        """

        return super(PocoTestCase, self).shortDescription()

    def defaultTestResult(self):
        return PocoTestResult()

    @classmethod
    def set_result_collector(cls, collector):
        cls._resule_collector = collector

    @classmethod
    def get_result_collector(cls):
        return cls._resule_collector

    @classmethod
    def add_result_emitter(cls, name, emitter):
        cls._result_emitters[name] = emitter

    @classmethod
    def get_result_emitter(cls, name):
        return cls._result_emitters.get(name)

    @classmethod
    def register_addon(cls, addon):
        cls._addons.append(addon)

    @classmethod
    def register_addin(cls, v):
        warnings.warn('`register_addin` is deprecated. Please use `register_addon` instead.')
        return cls.register_addon(v)

    @classmethod
    def get_assets_manager(cls):
        return cls._assets_manager

    def run(self, result=None):
        result = result or self.defaultTestResult()
        if not isinstance(result, PocoTestResult):
            raise TypeError('Test result class should be subclass of PocoTestResult. '
                            'Current test result instance is "{}".'.format(result))

        # register addon
        for addon in self._addons:
            addon.initialize(self)

        # start result emitter
        for name, emitter in self._result_emitters.items():
            try:
                emitter.start()
            except Exception as e:
                warnings.warn('Fail to start result emitter: "{}". Error message: "{}"'
                              .format(emitter.__class__.__name__, e.message))

        # run test
        ex = None
        ret = None
        try:
            ret = super(PocoTestCase, self).run(result)
        except Exception as e:
            ex = e

        assertionRecorder = self.get_result_emitter('assertionRecorder')
        for _, exc_type, e, tb in result.detail_errors:
            assertionRecorder.traceback(exc_type, e, tb)

        # stop result emitter
        for name, emitter in self._result_emitters.items():
            try:
                emitter.stop()
            except:
                pass

        # handle result
        if ex is not None:
            raise ex
        else:
            return ret

    def fail(self, msg=None):
        assertionRecorder = self.get_result_emitter('assertionRecorder')
        try:
            return super(PocoTestCase, self).fail(msg)
        except:
            exc_type, e, exc_tb = sys.exc_info()
            assertionRecorder.fail(msg, str(e), traceback.format_exc())
            raise exc_type, msg, exc_tb

    # assertions
    def assertTrue(self, expr, msg=None):
        assertionRecorder = self.get_result_emitter('assertionRecorder')
        assertionRecorder.assert_('True', [expr], msg)

        if not expr:
            msg = self._formatMessage(msg, "%s is not true" % safe_repr(expr))
            self.fail(msg)

    def assertFalse(self, expr, msg=None):
        assertionRecorder = self.get_result_emitter('assertionRecorder')
        assertionRecorder.assert_('False', [expr], msg)

        if expr:
            msg = self._formatMessage(msg, "%s is not false" % safe_repr(expr))
            self.fail(msg)

    def assertEqual(self, first, second, msg=None):
        assertionRecorder = self.get_result_emitter('assertionRecorder')
        assertionRecorder.assert_('Equal', [first, second], msg)
        return super(PocoTestCase, self).assertEqual(first, second, msg)

    def assertNotEqual(self, first, second, msg=None):
        assertionRecorder = self.get_result_emitter('assertionRecorder')
        assertionRecorder.assert_('NotEqual', [first, second], msg)
        return super(PocoTestCase, self).assertNotEqual(first, second, msg)

    def assertLess(self, a, b, msg=None):
        assertionRecorder = self.get_result_emitter('assertionRecorder')
        assertionRecorder.assert_('Less', [a, b], msg)
        return super(PocoTestCase, self).assertLess(a, b, msg)

    def assertLessEqual(self, a, b, msg=None):
        assertionRecorder = self.get_result_emitter('assertionRecorder')
        assertionRecorder.assert_('LessEqual', [a, b], msg)
        return super(PocoTestCase, self).assertLessEqual(a, b, msg)

    def assertGreater(self, a, b, msg=None):
        assertionRecorder = self.get_result_emitter('assertionRecorder')
        assertionRecorder.assert_('Greater', [a, b], msg)
        return super(PocoTestCase, self).assertGreater(a, b, msg)

    def assertGreaterEqual(self, a, b, msg=None):
        assertionRecorder = self.get_result_emitter('assertionRecorder')
        assertionRecorder.assert_('GreaterEqual', [a, b], msg)
        return super(PocoTestCase, self).assertGreaterEqual(a, b, msg)

    def assertIn(self, member, container, msg=None):
        assertionRecorder = self.get_result_emitter('assertionRecorder')
        assertionRecorder.assert_('In', [member, container], msg)
        return super(PocoTestCase, self).assertIn(member, container, msg)

    def assertNotIn(self, member, container, msg=None):
        assertionRecorder = self.get_result_emitter('assertionRecorder')
        assertionRecorder.assert_('NotIn', [member, container], msg)
        return super(PocoTestCase, self).assertNotIn(member, container, msg)
