from django import apps
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RiverConfig(AppConfig):
    name = 'georiviere.river'
    verbose_name = _("River")

    def ready(self):
        import georiviere.river.signals  # NOQA
        # Add a property with all Topologies model allowing to add all the elements linked with one stream
        from .models import Stream, TopologyMixin
        model_topologies = [model for model in apps.apps.get_models() if issubclass(model, TopologyMixin)]
        setattr(Stream, 'model_topologies', model_topologies)
