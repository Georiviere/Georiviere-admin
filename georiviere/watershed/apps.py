from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class WatershedConfig(AppConfig):
    name = 'georiviere.watershed'
    verbose_name = _("Watershed")
