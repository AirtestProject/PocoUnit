# coding=utf-8

from pocounit.addons import PocoUnitAddon


class ActionTracker(PocoUnitAddon):
    def __init__(self, poco):
        self.poco = poco
        self.action_recorder = None

    def initialize(self, Case):
        self.action_recorder = Case.get_result_emitter('actionRecorder')
        self.poco.add_pre_action_callback(self.on_pre_action)
        self.poco.add_post_action_callback(self.on_post_action)

    def on_pre_action(self, poco, action, proxy, args):
        tid = id(proxy)
        if action in ('click', 'long_click'):
            bounds = proxy.get_bounds()  # t r b l
            self.action_recorder.bounding(tid, bounds)
            self.action_recorder.click(tid, args, repr(proxy))
        elif action == 'swipe':
            bounds = proxy.get_bounds()
            self.action_recorder.bounding(tid, bounds)
            origin, direction = args
            self.action_recorder.swipe(tid, origin, direction, repr(proxy))

    def on_post_action(self, poco, action, proxy, args):
        tid = id(proxy)
        if action in ('click', 'long_click', 'swipe'):
            self.action_recorder.clear(tid)
