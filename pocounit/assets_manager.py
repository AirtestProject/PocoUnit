# coding=utf-8

import os


class AssetsManager(object):
    def __init__(self, project_root):
        super(AssetsManager, self).__init__()
        self.project_root = project_root

    def get_abspath(self, p):
        return os.path.join(self.project_root, p)

    get_resource_path = get_abspath
