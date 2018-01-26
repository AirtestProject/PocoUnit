# coding=utf-8

import sys
import traceback
import unittest

from unittest.util import safe_repr

from pocounit.result import PocoTestResult


class PocoTestCase(unittest.TestCase):
    """
    * longMessage: determines whether long messages (including repr of
        objects used in assert methods) will be printed on failure in *addition*
        to any explicit message passed.
    """
    longMessage = True

    testcase_assets_dir = '.'
    _resule_collector = None
    _result_emitters = {}  # name -> PocoTestResultEmitter
    _addins = []

    @classmethod
    def setUpClass(cls):
        """
        相当于airtest的pre脚本
        :return: 
        """

        pass

    def setUp(self):
        """
        初始化一个testcase
        不要把测试逻辑放到这里写，setUp报错的话也相当于真个case报错

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
        testcase的post脚本
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
    def set_testcase_assets_dir(cls, dirname):
        cls.testcase_assets_dir = dirname

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
    def register_addin(cls, addin):
        cls._addins.append(addin)

    def run(self, result=None):
        result = result or self.defaultTestResult()
        if not isinstance(result, PocoTestResult):
            raise TypeError('Test result class should be subclass of PocoTestResult. '
                            'Current test result instance is "{}".'.format(result))

        # register addin
        for addin in self._addins:
            addin.initialize(self)

        # start result emitter
        for name, emitter in self._result_emitters.items():
            emitter.start()

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
            emitter.stop()

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
