# coding=utf-8

from pocounit.result.emitter import PocoTestResultEmitter


class AppRuntimeLog(PocoTestResultEmitter):
    TAG = 'appRuntimeLog'

    def __init__(self, collector):
        super(AppRuntimeLog, self).__init__(collector)
        self.started = False

    def start(self):
        self.started = True

    def stop(self):
        self.started = False

    def log(self, content):
        if self.started:
            self.emit(self.TAG, {'content': content})
