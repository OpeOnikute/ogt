from __future__ import unicode_literals

from django.apps import AppConfig


class DashboardConfig(AppConfig):
    name = 'dashboard'

    def ready(self):
        from actstream import registry
        registry.register(self.get_model('Client'))
        registry.register(self.get_model('Job'))


