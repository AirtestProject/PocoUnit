# coding=utf-8

import sys


class Hooker(object):
    def __init__(self, func):
        self.pre_func = None
        self.hooked_func = func
        self.post_func = None
        self.exc_info = None

    def __call__(self, *args, **kwargs):
        if self.pre_func:
            self.pre_func(*args, **kwargs)

        ret = None
        try:
            ret = self.hooked_func(*args, **kwargs)
        except:
            self.exc_info = sys.exc_info()

        if self.post_func:
            self.post_func(ret, *args, **kwargs)

        if self.exc_info:
            raise self.exc_info
        else:
            return ret

    def pre(self, func):
        self.pre_func = func
        return func

    def post(self, func):
        self.post_func = func
        return func

    def __repr__(self):
        return '<{}.{} for {} object @+id/0x{}>'.format(self.__module__, self.__class__.__name__,
                                                        repr(self.hooked_func), hex(id(self)))
    __str__ = __repr__
