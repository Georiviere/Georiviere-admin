from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MaintenanceConfig(AppConfig):
    name = 'georiviere.maintenance'
    verbose_name = _("Maintenance")
