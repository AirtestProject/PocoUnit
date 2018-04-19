# coding=utf-8

import os
import inspect

from pocounit.assets_manager import AssetsManager
from pocounit.utils.misc import get_project_root


class FixtureUnit(object):
    _assets_manager = None

    def __init__(self):
        test_case_filename = os.path.abspath(inspect.getsourcefile(self.__class__))
        test_case_dir = os.path.dirname(test_case_filename)
        project_root = get_project_root(test_case_filename)
        print('using "{}" as project root. This testcase is "{}"'.format(project_root, self.__class__.__name__))
        self.set_assets_manager(AssetsManager(project_root))

        self.test_case_filename = test_case_filename
        self.test_case_dir = test_case_dir
        self.project_root = project_root

    def setUp(self):
        """
        初始化一个testcase
        不要把测试逻辑放到这里写，setUp报错的话也相当于整个case报错

        """

        pass

    def tearDown(self):
        """
        一个testcase的清场工作

        """

        pass

    @classmethod
    def set_assets_manager(cls, v):
        if type(cls) is not type:
            cls = cls.__class__
        cls._assets_manager = v

    @classmethod
    def get_assets_manager(cls):
        return cls._assets_manager

    @classmethod
    def R(cls, respath):
        return cls._assets_manager.get_resource_path(respath)
