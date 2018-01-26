# coding=utf-8

import sys
from unittest.runner import TextTestResult


class PocoTestResult(TextTestResult):
    def __init__(self, stream=sys.stderr, descriptions=True, verbosity=1):
        super(PocoTestResult, self).__init__(stream, descriptions, verbosity)
        self.detail_errors = []

    def addError(self, test, err):
        exc_type, e, exc_tb = err
        self.detail_errors.append((test, exc_type, e, exc_tb))
        return super(PocoTestResult, self).addError(test, err)
