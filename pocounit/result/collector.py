# coding=utf-8

import os
import time
import json

from pocounit.result.logger import StreamLogger


class PocoResultCollector(object):
    def __init__(self, project_root, testcases_filenames, testcase_name, testcase_dir='.', logfilename='poco-result.log'):
        self.testcases_filenames = testcases_filenames  # [full path], multiple files
        self.testcase_dir = testcase_dir
        self.project_root = project_root

        root_paths = [project_root, 'pocounit-results']
        root_paths += os.path.relpath(testcase_dir, project_root).replace('\\', '/').split('/')
        root_paths.append(os.path.splitext(os.path.basename(testcases_filenames[0]))[0])
        root_paths.append(testcase_name)

        self.root = os.path.join(*root_paths)
        if os.path.isfile(self.root):
            raise RuntimeError('"{}" already exists as non-directory, please remove it first.')
        if not os.path.exists(self.root):
            os.makedirs(self.root)
        self.logger = StreamLogger(os.path.join(self.root, logfilename))

    def collect(self, tag, value):
        self.logger.write(json.dumps({'tag': tag, 'value': value, 'ts': time.time()}))

    def get_root_path(self):
        return self.root

    def get_project_root_path(self):
        return self.project_root

    def get_resource_relative_path(self, respath):
        return os.path.relpath(respath, self.root)

    def get_testcases_filenames(self):
        return self.testcases_filenames

    def add_testcase_file(self, path):
        """
        除了TestCase class所定义的那个文件之外，的其他关联的文件都可以加进来

        :param path:
        :return:
        """

        path = os.path.join(self.project_root, path)
        self.testcases_filenames.append(path)
