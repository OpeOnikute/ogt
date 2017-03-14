from __future__ import unicode_literals
from django.apps import AppConfig, apps


class DashboardConfig(AppConfig):
    name = 'dashboard'

    def ready(self):
        from actstream import registry
        registry.register(apps.get_model('auth.user'))
        registry.register(self.get_model('Client'))
        registry.register(self.get_model('Job'))
        registry.register(self.get_model('DesignProblems'))
        registry.register(self.get_model('PotentialClient'))
        registry.register(self.get_model('PotentialProject'))
        registry.register(self.get_model('Inspiration'))
        registry.register(self.get_model('Client'))
        registry.register(self.get_model('Task'))


