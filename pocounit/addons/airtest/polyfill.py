# coding=utf-8


def preload_airtest_device_context(run_on_win=False, window_title='^.*errors and.*$'):
    from airtest.cli.runner import device as current_device
    if not current_device():
        from airtest.core.main import set_serialno, set_windows
        from airtest.core.settings import Settings
        from airtest.core.android.adb import ADB
        adb_client = ADB()
        available_devices = adb_client.devices('device')
        if run_on_win or not available_devices:
            Settings.FIND_INSIDE = [8, 30]  # 窗口边框偏移
            set_windows(window_title=window_title)
        else:
            set_serialno()
        exec("from airtest.core.main import *") in globals()


