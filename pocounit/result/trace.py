# coding=utf-8

import os
import sys
import shutil

from pocounit.result.emitter import PocoTestResultEmitter


class ScriptTracer(PocoTestResultEmitter):
    TAG = 'trace'

    def __init__(self, collector):
        super(ScriptTracer, self).__init__(collector)
        self.project_root = self.collector.get_project_root_path()
        self.script_filenames = self.collector.get_testcases_filenames()
        self.script_filenames_lower = None

    def start(self):
        self.script_filenames_lower = [f.lower() for f in self.script_filenames]
        for f in self.script_filenames:
            src = os.path.relpath(f, self.project_root)
            dst = os.path.join(self.collector.get_root_path(), src)
            dst_dir = os.path.dirname(dst)
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            shutil.copyfile(f, dst)
        sys.settrace(self.make_tracer())

    def make_tracer(self):
        def tracer(frame, event, arg):
            if event == 'line' and frame.f_code.co_filename.lower() in self.script_filenames_lower:
                line_num = frame.f_lineno
                fname = os.path.relpath(frame.f_code.co_filename, self.project_root)
                self.emit(self.TAG, {'filename': fname, 'lineno': line_num})  # 暂时忽略不同路径同名的情况
            return tracer
        return tracer
