# coding=utf-8

import sys

from pocounit.result.emitter import PocoTestResultEmitter


class Redirector(object):
    def __init__(self, origin, _type, logger):
        super(Redirector, self).__init__()
        self.buf = ''
        self.type = _type
        self.logger = logger
        if hasattr(sys, '__save_origin_std_' + _type):
            self.origin = getattr(sys, '__save_origin_std_' + _type)
        else:
            self.origin = origin
            setattr(sys, '__save_origin_std_' + _type, origin)

    def write(self, text):
        # 如果原流不支持unicode，那就忽略
        try:
            self.origin.write(text)
        except:
            pass

        self.buf += text
        lines = None
        if self.buf.endswith('\n'):
            lines, self.buf = self.buf.rstrip(), ''
        elif '\n' in self.buf:
            lines, self.buf = self.buf.rsplit('\n', 1)

        if lines:
            self.logger.log(lines)

    def __getattr__(self, key):
        if hasattr(self.origin, key):
            return getattr(self.origin, key)
        else:
            raise AttributeError('{} has no attribute {}'.format(self.origin, key))


class RunnerRuntimeLog(PocoTestResultEmitter):
    TAG = 'runnerRuntimeLog'

    def __init__(self, collector):
        super(RunnerRuntimeLog, self).__init__(collector)

    def start(self):
        if not hasattr(sys, '__redirected_stdout'):
            setattr(sys, '__redirected_stdout', sys.stdout)
            sys.stdout = Redirector(sys.stdout, 'stdout', self)
        if not hasattr(sys, '__redirected_stderr'):
            setattr(sys, '__redirected_stderr', sys.stderr)
            sys.stderr = Redirector(sys.stderr, 'stderr', self)

    def stop(self):
        if hasattr(sys, '__redirected_stdout'):
            sys.stdout = sys.stdout.origin
            delattr(sys, '__redirected_stdout')
        if hasattr(sys, '__redirected_stderr'):
            sys.stderr = sys.stderr.origin
            delattr(sys, '__redirected_stderr')

    def log(self, content):
        self.emit(self.TAG, {'content': content})
