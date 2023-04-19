from django.utils.translation import gettext_lazy as _
from mapentity.registry import MapEntityOptions


class ValorizationOptions(MapEntityOptions):
    def __init__(self, model):
        super(ValorizationOptions, self).__init__(model)
        self.label = _('Valorization')
