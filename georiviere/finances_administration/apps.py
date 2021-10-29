from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FinancesAdministrationConfig(AppConfig):
    name = 'georiviere.finances_administration'
    verbose_name = _("Finances and administration")
