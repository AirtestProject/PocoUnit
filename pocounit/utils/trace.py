# coding=utf-8

import sys


def get_current_lineno_of(filenames, frame=None):
    filenames_lower = [f.lower().replace('\\', '/') for f in filenames]

    frame = frame or sys._getframe(0)
    while frame:
        if frame.f_code.co_filename.lower().replace('\\', '/') in filenames_lower:
            break
        frame = frame.f_back

    if frame:
        return frame.f_lineno, frame.f_code.co_filename
    else:
        return None, None
