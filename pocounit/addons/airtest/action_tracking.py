# coding=utf-8

import inspect
import sys
import traceback

from pocounit.addons import PocoUnitAddon
from pocounit.addons.airtest.utils import Hooker

from airtest.core.main import loop_find, touch, swipe, exists, assert_exists
from airtest.core.cv import _cv_match
from airtest.core.helper import MoaPic as Target
from airtest.cli.runner import device as current_device


class ActionTracker(PocoUnitAddon):
    """
    general airtest action pattern and invocation stack

    |  touch start
    |    loop find
    |      cv match, return match result
    |  touch end

    """

    def __init__(self):
        self.action_recorder = None
        self.assertion_recorder = None
        self._doing_actions = False  # 在touch或swipe中时设为true

        self.loop_find_ = Hooker(loop_find)
        self.touch_ = Hooker(touch)
        self._cv_match_ = Hooker(_cv_match)
        self.assert_exists_ = Hooker(assert_exists)

        self.touch_.pre(self.pre_touch)
        self.touch_.post(self.post_touch)
        self.loop_find_.post(self.post_loop_find)
        self._cv_match_.post(self.post_cv_match)
        self.assert_exists_.pre(self.pre_assert_exists)
        self.assert_exists_.post(self.post_assert_exists)

        import airtest.core.main as acm
        import airtest.core.cv as acc
        acm.touch = self.touch_
        acm.loop_find = self.loop_find_
        acm.assert_exists = self.assert_exists_
        acc._cv_match = self._cv_match_

    def initialize(self, Case):
        self.action_recorder = Case.get_result_emitter('actionRecorder')
        self.assertion_recorder = Case.get_result_emitter('assertionRecorder')

        frame = sys._getframe(0)
        while frame.f_back is not None:
            frame.f_globals['touch'] = self.touch_
            frame.f_globals['loop_find'] = self.loop_find_
            frame.f_globals['assert_exists'] = self.assert_exists_
            frame = frame.f_back

    def post_loop_find(self, pos, v, *args, **kwargs):
        if pos is not None and isinstance(v, Target):
            w, h = current_device().getCurrentScreenResolution()
            x, y = pos
            tid = id(v)
            if self._doing_actions:
                self.action_recorder.click(tid, [1.0 * x / w, 1.0 * y / h], v.filepath)

    def post_cv_match(self, cv_ret, *args, **kwargs):
        if not cv_ret:
            return

        # 如果当前函数是由loop_find调用的，那就可以找到一个rect，这个rect由airtest.core.cv._cv_match里给出
        # 以下就是从frame stack中一直找到loop_find这一帧，然后找出loop_find的第一个argument，通过argument求出tid
        frame = sys._getframe(0)
        while frame and frame.f_code.co_name != 'loop_find':
            frame = frame.f_back
        if frame:
            # more details about inspect parameter name in runtime,
            # see https://docs.python.org/2/library/inspect.html#inspect.getargvalues
            args, varargs, keywords, locals = inspect.getargvalues(frame)
            if len(args) > 0:
                v_name = args[0]
            elif varargs is not None and len(locals[varargs]) > 0:
                v_name = locals[varargs][0]
            else:
                raise ValueError('loop_find第一个参数不支持使用keyword args')

            # 取到loop_find的第一个argument
            v = locals[v_name]
            tid = id(v)
            rect = cv_ret.get("rectangle")
            if rect:
                # a rect's each vertex in screen as following
                # [0]  [3]
                # [1]  [2]
                t = rect[0][1] * 1.0
                r = rect[3][0] * 1.0
                b = rect[1][1] * 1.0
                l = rect[0][0] * 1.0
                w, h = current_device().getCurrentScreenResolution()
                self.action_recorder.bounding(tid, [t / h, r / w, b / h, l / w])

    def pre_touch(self, v, *args, **kwargs):
        self._doing_actions = True
        if isinstance(v, (list, tuple)):
            tid = id(v)
            w, h = current_device().getCurrentScreenResolution()
            x, y = v
            self.action_recorder.click(tid, [1.0 * x / w, 1.0 * y / h], 'fixed point: {}'.format(v))

    def post_touch(self, ret, v, *args, **kwargs):
        self._doing_actions = False
        if isinstance(v, (Target, list, tuple)):
            tid = id(v)
            self.action_recorder.clear(tid)
            return

    def pre_assert_exists(self, v, message, *args, **kwargs):
        if isinstance(v, Target):
            pass

    def post_assert_exists(self, ret, v, message, *args, **kwargs):
        if isinstance(v, Target):
            tid = id(v)
            self.assertion_recorder.assert_('Existence', [v.filename], message)
            self.action_recorder.clear(tid)
