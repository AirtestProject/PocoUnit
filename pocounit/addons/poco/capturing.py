# coding=utf-8

from pocounit.addons import PocoUnitAddon


class SiteCaptor(PocoUnitAddon):
    def __init__(self, poco):
        super(SiteCaptor, self).__init__()
        self.poco = poco
        self.site_snapshot = None

    def initialize(self, Case):
        self.site_snapshot = Case.get_result_emitter('siteSnapshot')
        self.site_snapshot.set_poco_instance(self.poco)

    def snapshot(self, site_id):
        return self.site_snapshot.snapshot(site_id)
