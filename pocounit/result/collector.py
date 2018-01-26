# coding=utf-8

import os
import time
import json

from pocounit.result.logger import StreamLogger


class PocoResultCollector(object):
    def __init__(self, project_root, testcases_filenames, testcase_dir='.', logfilename='poco-result.log'):
        self.testcases_filenames = testcases_filenames  # [full path], multiple files
        self.testcase_dir = testcase_dir
        self.project_root = project_root
        self.root = os.path.abspath(os.path.join(testcase_dir, 'result'))
        if os.path.isfile(self.root):
            raise RuntimeError('"{}" already exists as non-directory, please remove it.')
        if not os.path.exists(self.root):
            os.mkdir(self.root)
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
        path = os.path.abspath(path)
        self.testcases_filenames.append(path)
