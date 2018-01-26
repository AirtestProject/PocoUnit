# coding=utf-8


class PocoTestResultEmitter(object):
    def __init__(self, collector):
        self.collector = collector

    def start(self):
        pass

    def stop(self):
        pass

    def finalize(self):
        pass

    def emit(self, tag, value):
        self.collector.collect(tag, value)
