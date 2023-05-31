from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PortalConfig(AppConfig):
    name = 'georiviere.portal'
    verbose_name = _("Portal")

    def ready(self):
        import georiviere.portal.signals  # NOQA
