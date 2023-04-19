from django_filters import CharFilter
from django.utils.translation import gettext_lazy as _
from mapentity.filters import MapEntityFilterSet

from georiviere.valorization.models import POIKnowledge, POIAction

from georiviere.watershed.filters import WatershedFilterSet

from geotrek.zoning.filters import ZoningFilterSet


class POIKnowledgeFilterSet(WatershedFilterSet, ZoningFilterSet, MapEntityFilterSet):
    name = CharFilter(label=_('Name'), lookup_expr='icontains')

    class Meta(MapEntityFilterSet.Meta):
        model = POIKnowledge
        fields = MapEntityFilterSet.Meta.fields + ['name', 'type']


class POIActionFilterSet(WatershedFilterSet, ZoningFilterSet, MapEntityFilterSet):
    name = CharFilter(label=_('Name'), lookup_expr='icontains')

    class Meta(MapEntityFilterSet.Meta):
        model = POIAction
        fields = MapEntityFilterSet.Meta.fields + ['name', 'type']
