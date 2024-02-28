from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from django.apps import apps

from django.db.models.signals import post_delete, post_save


class MainConfig(AppConfig):
    name = 'georiviere.main'
    verbose_name = _("Main")

    def ready(self):
        from . import signals
        from mapentity.models import MapEntityMixin
        from georiviere.river.models import Stream
        for model in apps.get_models():
            if issubclass(model, MapEntityMixin) and model != Stream:
                print("signal for model {}".format(model))
                post_save.connect(signals.save_objects_generate_distance_to_source, sender=model)
                post_delete.connect(signals.delete_objects_remove_distance_to_source, sender=model)
