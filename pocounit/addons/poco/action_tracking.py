# coding=utf-8

from pocounit.addons import PocoUnitAddon


class ActionTracker(PocoUnitAddon):
    def __init__(self, poco):
        super(ActionTracker, self).__init__()
        self.poco = poco
        self.action_recorder = None

    def initialize(self, Case):
        self.action_recorder = Case.get_result_emitter('actionRecorder')
        self.poco.add_pre_action_callback(self.on_pre_action)
        self.poco.add_post_action_callback(self.on_post_action)

    def on_pre_action(self, poco, action, ui, args):
        tid = id(ui)
        if action in ('click', 'long_click'):
            bounds = ui.get_bounds()  # t r b l
            self.action_recorder.bounding(tid, bounds)
            self.action_recorder.click(tid, args, repr(ui))
        elif action == 'swipe':
            bounds = ui.get_bounds()
            self.action_recorder.bounding(tid, bounds)
            origin, direction = args
            self.action_recorder.swipe(tid, origin, direction, repr(ui))

    def on_post_action(self, poco, action, ui, args):
        tid = id(ui)
        if action in ('click', 'long_click', 'swipe'):
            self.action_recorder.clear(tid)
