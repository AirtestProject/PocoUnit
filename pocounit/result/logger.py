# coding=utf-8

import threading


class StreamLogger(object):
    def __init__(self, filename='poco-stream-result.log'):
        self.logfile = open(filename, 'w')
        self.mutex = threading.Lock()

    def write(self, val):
        with self.mutex:
            self.logfile.write(val)
            self.logfile.write('\n')
            self.logfile.flush()
