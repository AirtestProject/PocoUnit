# coding=utf-8

import datetime

from pocounit.result.emitter import PocoTestResultEmitter


class MetaInfo(PocoTestResultEmitter):
    TAG = 'MetaInfo'

    def __init__(self, collector):
        super(MetaInfo, self).__init__(collector)

    def test_started(self, name):
        self.emit(self.TAG, {
            'type': 'testcase',
            'value': {
                'name': name,
                'started_at': str(datetime.datetime.now()),
            }
        })

    def test_ended(self, name):
        self.emit(self.TAG, {
            'type': 'testcase',
            'value': {
                'name': name,
                'ended_at': str(datetime.datetime.now()),
            }
        })

    def test_succeed(self, name):
        self.emit(self.TAG, {
            'type': 'testcase',
            'value': {
                'name': name,
                'success': True,
            }
        })

    def test_fail(self, name):
        self.emit(self.TAG, {
            'type': 'testcase',
            'value': {
                'name': name,
                'success': False,
            }
        })

    def set_testcase_metainfo(self, name, metainfo):
        self.emit(self.TAG, {
            'type': 'testcase',
            'value': {
                'name': name,
                'metainfo': metainfo,
            }
        })

    def snapshot_device_info(self, udid, info):
        """
        Take down the device info according udid.

        :param udid: serialno for Android
        :param info: a dict hold any information of the device
        """

        self.emit(self.TAG, {
            'type': 'device',
            'value': {
                'udid': udid,
                'info': info,
            }
        })

    def emit(self, tag, value):
        self.collector.collect_metainfo(tag, value)
