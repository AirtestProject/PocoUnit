# coding=utf-8

from pocounit.result.emitter import PocoTestResultEmitter


class AppRuntimeLog(PocoTestResultEmitter):
    TAG = 'appRuntimeLog'

    def log(self, content):
        self.emit(self.TAG, {'content': content})
