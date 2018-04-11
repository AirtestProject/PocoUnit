# coding=utf-8

import os

from pocounit.result.emitter import PocoTestResultEmitter
from airtest.core.api import device as current_device


class ScreenRecorder(PocoTestResultEmitter):
    TAG = 'record'

    def __init__(self, collector, device=None):
        super(ScreenRecorder, self).__init__(collector)
        self.device = device or current_device()
        self.record_filepath = os.path.join(self.collector.get_root_path(), 'screen.mp4')
        self.started = False

    def start(self):
        if self.started:
            return False
        self.started = True

        self.device = self.device or current_device()
        if self.device and hasattr(self.device, 'start_recording'):
            try:
                # force to stop before starting new recoding
                self.device.stop_recording(self.record_filepath)
            except:
                pass

            success = self.device.start_recording()
            if success:
                relpath = self.collector.get_resource_relative_path(self.record_filepath)
                display_info = self.device.display_info
                if display_info['orientation'] in (1, 3):
                    orientation = 'horizontal'
                    resolution = [display_info['height'], display_info['width']]
                else:
                    orientation = 'vertical'
                    resolution = [display_info['width'], display_info['height']]

                # orientation: current orientation
                # resolution: recording resolution. 当前默认等于屏幕分辨率
                self.emit(self.TAG, {'event': 'started', 'filename': relpath, 'orientation': orientation, 'resolution': resolution})
            return success
        return False

    def stop(self):
        if not self.started:
            return False
        self.started = False

        self.device = self.device or current_device()
        if self.device and hasattr(self.device, 'stop_recording'):
            self.emit(self.TAG, {'event': 'stopped'})
            try:
                return self.device.stop_recording(self.record_filepath)
            except:
                try:
                    # 如果停止失败，就尝试直接pull最后一次录屏文件
                    return self.device.recorder.pull_last_recording_file(self.record_filepath)
                except:
                    pass
        return False
