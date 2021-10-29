from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ObservationsConfig(AppConfig):
    name = 'georiviere.observations'
    verbose_name = _("Observations")
