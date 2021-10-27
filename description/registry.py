from django.utils.translation import gettext_lazy as _
from mapentity.registry import MapEntityOptions


class DescriptionOptions(MapEntityOptions):
    def __init__(self, model):
        super(DescriptionOptions, self).__init__(model)
        self.label = _('Descriptions')
