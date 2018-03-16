# coding=utf-8

import os
import traceback

from pocounit.result.emitter import PocoTestResultEmitter
from pocounit.utils.trace import get_current_lineno_of


class AssertionRecorder(PocoTestResultEmitter):
    TAG = 'assertion'

    def assert_(self, assertionType, args, assertionMsg):
        lineno, srcfilename = get_current_lineno_of(self.collector.get_testcases_filenames())
        self.emit(self.TAG, {'method': 'assert', 'type': assertionType, 'args': args, 'msg': assertionMsg,
                             'lineno': lineno, 'srcfilename': srcfilename})

    def fail(self, errmsg, assertionMsg, tb):
        lineno, srcfilename = get_current_lineno_of(self.collector.get_testcases_filenames())
        self.emit(self.TAG, {'method': 'fail', 'errmsg': errmsg, 'msg': assertionMsg, 'traceback': tb,
                             'lineno': lineno, 'srcfilename': srcfilename})

    def traceback(self, errtype, e, tb):
        # tb1 用来获取最近报错调用帧栈
        # tb用来format一个完整的tb
        # 去到离现场最近的tb位置
        tb1 = tb
        tb_stack = [tb1]
        while tb1.tb_next:
            tb1 = tb1.tb_next
            tb_stack.append(tb1)

        # 跳过unittest相关的tb frame
        while tb and '__unittest' in tb.tb_frame.f_globals:
            tb = tb.tb_next

        lineno, srcfilename = None, None
        if tb:
            while tb_stack:
                lineno, srcfilename = get_current_lineno_of(self.collector.get_testcases_filenames(), tb_stack.pop().tb_frame)
                if srcfilename:
                    break
            if srcfilename:
                srcfilename = os.path.relpath(srcfilename, self.collector.get_project_root_path())
            formatted_tb = ''.join(traceback.format_exception(errtype, e, tb))
        else:
            formatted_tb = ''
        self.emit(self.TAG, {'method': 'traceback', 'errtype': errtype.__name__, 'traceback': formatted_tb,
                             'lineno': lineno, 'srcfilename': srcfilename})
