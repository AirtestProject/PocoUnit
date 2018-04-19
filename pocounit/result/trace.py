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
        self._script_filenames = None
        self._script_filenames_lower = None
        self._origin_trace_func = None

    def start(self):
        self._script_filenames = self.collector.get_testcases_filenames()
        self._script_filenames_lower = [f.lower().replace('\\', '/') for f in self._script_filenames]
        for f in self._script_filenames:
            src = os.path.relpath(f, self.project_root)
            dst = os.path.join(self.collector.get_root_path(), src)
            dst_dir = os.path.dirname(dst)
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            shutil.copyfile(f, dst)
        self._origin_trace_func = sys.gettrace()
        sys.settrace(self._make_tracer())

    def stop(self):
        sys.settrace(self._origin_trace_func)

    def _make_tracer(self):
        def tracer(frame, event, arg):
            co_filename = frame.f_code.co_filename
            if event == 'line' and co_filename.lower().replace('\\', '/') in self._script_filenames_lower:
                line_num = frame.f_lineno
                fname = os.path.relpath(co_filename, self.project_root)
                fname = fname.replace('\\', '/')
                self.emit(self.TAG, {'filename': fname, 'lineno': line_num})
            return tracer
        return tracer
