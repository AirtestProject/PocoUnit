# coding=utf-8

import unittest

from pocounit.result import PocoTestResult


class PocoTestRunner(unittest.TextTestRunner):
    """
    先占坑，先默认用text方式展示，以后再换成自定义的    
    """

    resultclass = PocoTestResult
