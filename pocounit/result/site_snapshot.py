# coding-utf-8

import base64
import hashlib
import time
import json
import os
import six

from pocounit.result.emitter import PocoTestResultEmitter


def make_hash(src):
    if isinstance(src, six.text_type):
        src = src.encode('utf-8')
    else:
        src = six.binary_type(src)
    return hashlib.md5(src).hexdigest()


class SiteSnapshot(PocoTestResultEmitter):
    TAG = 'siteSnapshot'

    def __init__(self, collector):
        super(SiteSnapshot, self).__init__(collector)
        self.save_path = os.path.join(collector.get_root_path(), 'snapshots')
        if not os.path.exists(self.save_path):
            os.mkdir(self.save_path)
        self.poco = None

    def stop(self):
        self.snapshot('caseEnd')

    def set_poco_instance(self, poco):
        self.poco = poco

    def snapshot(self, site_id=None):
        self.snapshot_screen(site_id)
        self.snapshot_hierarchy(site_id)

    def snapshot_hierarchy(self, site_id=None):
        if not self.poco:
            return
        site_id = site_id or time.time()
        hierarchy_data = self.poco.agent.hierarchy.dump()
        basename = 'hierarchy-{}.json'.format(make_hash(site_id))
        fpath = os.path.join(self.save_path, basename)
        with open(fpath, 'wb') as f:
            h = json.dumps(hierarchy_data)
            if six.PY3:
                h = h.encode('utf-8')
            f.write(h)
        self.emit(self.TAG, {'type': 'hierarchy', 'dataPath': 'snapshots/{}'.format(basename), 'site_id': site_id})
        return fpath

    def snapshot_screen(self, site_id=None):
        if not self.poco:
            return
        site_id = site_id or time.time()
        b64img, fmt = self.poco.snapshot()
        width, height = self.poco.get_screen_size()
        basename = 'screen-{}.{}'.format(make_hash(site_id), fmt)
        fpath = os.path.join(self.save_path, basename)
        with open(fpath, 'wb') as f:
            f.write(base64.b64decode(b64img))
        self.emit(self.TAG, {'type': 'screen', 'dataPath': 'snapshots/{}'.format(basename), 'site_id': site_id,
                             'width': width, 'height': height, 'format': fmt})
        return fpath
