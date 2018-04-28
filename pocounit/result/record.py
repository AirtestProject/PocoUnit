# coding=utf-8

import os

from pocounit.result.emitter import PocoTestResultEmitter
from airtest.core.api import device as current_device
from airtest.core.helper import G


def get_udid(dev):
    if hasattr(dev, 'serialno'):
        return dev.serialno
    raise TypeError('Cannot get udid from {}'.format(repr(dev)))


# 多设备录屏待测试
class ScreenRecorder(PocoTestResultEmitter):
    TAG = 'record'

    def __init__(self, collector, devices=None):
        super(ScreenRecorder, self).__init__(collector)
        self.devices = devices
        self.record_filepaths = {}  # udid -> path
        self.started = {}  # udid -> True/False

    def start(self):
        if self.started:
            return False

        # initialize details
        self.devices = self.devices or G.DEVICE_LIST
        for dev in self.devices:
            udid = get_udid(dev)
            self.record_filepaths[udid] = os.path.join(self.collector.get_root_path(), 'screen-{}.mp4'.format(udid))

        # start recording
        for dev in self.devices:
            udid = get_udid(dev)
            self.started[udid] = self.start_device_recorder(udid, dev)

        return True

    def stop(self):
        if not self.started:
            return False

        for dev in self.devices:
            udid = get_udid(dev)
            if self.started[udid]:
                self.stop_device_recorder(udid, dev)
                del self.started[udid]

        return True

    def start_device_recorder(self, udid, device):
        record_file = self.record_filepaths[udid]
        if hasattr(device, 'start_recording') and hasattr(device, 'stop_recording'):
            try:
                # force to stop before starting new recoding
                device.stop_recording(record_file)
            except:
                pass

            success = device.start_recording()
            if success:
                relpath = self.collector.get_resource_relative_path(record_file)
                display_info = device.display_info
                if display_info['orientation'] in (1, 3):
                    orientation = 'horizontal'
                    resolution = [display_info['height'], display_info['width']]
                else:
                    orientation = 'vertical'
                    resolution = [display_info['width'], display_info['height']]

                # orientation: current orientation
                # resolution: recording resolution. 当前默认等于屏幕分辨率
                relpath = relpath.replace('\\', '/')
                self.emit(self.TAG, {'event': 'started', 'filename': relpath, 'orientation': orientation, 'resolution': resolution})
            return success
        return False

    def stop_device_recorder(self, udid, device):
        if hasattr(device, 'stop_recording'):
            record_file = self.record_filepaths[udid]
            relpath = self.collector.get_resource_relative_path(record_file).replace('\\', '/')
            self.emit(self.TAG, {'event': 'stopped', 'filename': relpath})

            try:
                return device.stop_recording(record_file)
            except:
                try:
                    # 如果停止失败，就尝试直接pull最后一次录屏文件
                    return device.recorder.pull_last_recording_file(record_file)
                except:
                    pass
        return False
