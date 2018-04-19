# coding=utf-8

from pocounit.case import PocoTestCase
from pocounit.addons.poco.action_tracking import ActionTracker

from poco.drivers.android.uiautomation import AndroidUiautomationPoco


class AndroidNativeUITestCase(PocoTestCase):
    @classmethod
    def setUpClass(cls):
        super(AndroidNativeUITestCase, cls).setUpClass()

        cls.poco = AndroidUiautomationPoco()

        # 启用动作捕捉(action tracker)和游戏运行时日志捕捉插件(runtime logger)
        action_tracker = ActionTracker(cls.poco)
        cls.register_addon(action_tracker)


class T1(AndroidNativeUITestCase):
    def runTest(self):
        self.poco(text='设置').click()
        self.poco(text='WLAN').click()


if __name__ == '__main__':
    import pocounit
    pocounit.main()
