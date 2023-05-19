from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ContributionConfig(AppConfig):
    name = 'georiviere.contribution'
    verbose_name = _("contribution")
