from django_filters import CharFilter
from django.utils.translation import gettext_lazy as _
from mapentity.filters import MapEntityFilterSet, PythonPolygonFilter
from geotrek.zoning.filters import ZoningFilterSet

from georiviere.knowledge.models import Knowledge, FollowUp
from georiviere.watershed.filters import WatershedFilterSet


class KnowledgeFilterSet(WatershedFilterSet, ZoningFilterSet, MapEntityFilterSet):
    name = CharFilter(label=_('Name'), lookup_expr='icontains')
    code = CharFilter(label=_('Code'), lookup_expr='icontains')

    class Meta(MapEntityFilterSet.Meta):
        model = Knowledge
        fields = MapEntityFilterSet.Meta.fields + ['knowledge_type']


class FollowUpFilterSet(WatershedFilterSet, ZoningFilterSet, MapEntityFilterSet):
    bbox = PythonPolygonFilter(field_name='geom')
    name = CharFilter(label=_('Name'), lookup_expr='icontains')

    class Meta(MapEntityFilterSet.Meta):
        model = FollowUp
        fields = MapEntityFilterSet.Meta.fields + [
            'name',
            'followup_type',
            'knowledge',
        ]
