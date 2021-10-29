from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MainConfig(AppConfig):
    name = 'georiviere.main'
    verbose_name = _("Main")
