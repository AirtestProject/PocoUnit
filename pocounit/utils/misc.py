# coding=utf-8

import os
import re


def detect_package_root(mod_filename):
    """
    从某个模块的文件路径向上搜索，一直找到这个模块所在包的根目录，将包名第一段返回

    :param mod_filename:
    :return: 根包名 or None
    """

    egginfo_pattern = re.compile(r'.*\.egg-info$')
    p = os.path.abspath(os.path.join(mod_filename, '..'))
    while True:
        ls = os.listdir(p)
        matched = False
        for f in ls:
            if f == 'setup.py' or egginfo_pattern.match(f):
                matched = True
                break
        if matched:
            break
        p_prev = os.path.abspath(os.path.join(p, '..'))
        if p == p_prev:
            return None
        p = p_prev
    return p


def get_project_root(test_case_filename):
    return os.getenv("PROJECT_ROOT") or detect_package_root(test_case_filename) or os.getcwd()


def has_override(method, subCls, baseCls):
    return getattr(subCls, method).__func__ is not getattr(baseCls, method).__func__
