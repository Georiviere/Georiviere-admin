from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class StudiesConfig(AppConfig):
    name = 'georiviere.studies'
    verbose_name = _("Studies")
