# coding=utf-8

from pocounit.result.emitter import PocoTestResultEmitter
from pocounit.utils.trace import get_current_lineno_of


class ActionRecorder(PocoTestResultEmitter):
    TAG = 'action'

    def motion(self, tid, desc, points):
        """
        记录motion event，一个motion event就是一个点的轨迹，比如从A拖动到B，每个motion event使用tid分组，同一个tid分组的会归并在一起，
        多点触控的两组轨迹就必须是相同的tid，调用两次这个方法并传入相同的tid即可

        :param tid: event 分组标号
        :param desc: 事件描述
        :param points: 点序列，按顺序构成一系列轨迹
        :return: None
        """

        lineno, srcfilename = get_current_lineno_of(self.collector.get_testcases_filenames())
        self.emit(self.TAG, {'action': 'click', 'tid': tid, 'targetDescription': desc, 'points': points,
                             'lineno': lineno, 'srcfilename': srcfilename})

    def key(self, tid, keyname):
        """
        记录一个按键事件

        :param tid: 事件编号，配合clear清除 
        :param keyname:  按键键名，如 A B Enter等
        :return: None
        """

        raise NotImplementedError

    def click(self, tid, pos, desc):
        lineno, srcfilename = get_current_lineno_of(self.collector.get_testcases_filenames())
        self.emit(self.TAG, {'action': 'click', 'tid': tid, 'origin': pos, 'targetDescription': desc,
                             'lineno': lineno, 'srcfilename': srcfilename})

    def swipe(self, tid, origin, direction, desc):
        lineno, srcfilename = get_current_lineno_of(self.collector.get_testcases_filenames())
        self.emit(self.TAG, {'action': 'swipe', 'tid': tid, 'origin': origin, 'direction': direction, 'targetDescription': desc,
                             'lineno': lineno, 'srcfilename': srcfilename})

    def bounding(self, tid, bound):
        self.emit(self.TAG, {'action': 'bounding', 'tid': tid, 'bounds': bound})

    def clear(self, tid):
        self.emit(self.TAG, {'action': 'clear', 'tid': tid})
