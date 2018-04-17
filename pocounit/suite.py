# coding=utf-8

import unittest

from pocounit.fixture import FixtureUnit


class PocoTestSuite(unittest.TestSuite, FixtureUnit):
    def __init__(self, tests=()):
        unittest.TestSuite.__init__(self, tests)
        FixtureUnit.__init__(self)

    def run(self, result, debug=False):
        self.setUp()
        super(PocoTestSuite, self).run(result, debug)
        self.tearDown()
