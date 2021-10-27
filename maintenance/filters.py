from django_filters import CharFilter
from django.utils.translation import gettext_lazy as _

from mapentity.filters import MapEntityFilterSet, PythonPolygonFilter
from geotrek.zoning.filters import ZoningFilterSet

from maintenance.models import Intervention
from main.filters import RestrictedAreaFilterSet
from watershed.filters import WatershedFilterSet


class InterventionFilterSet(WatershedFilterSet, RestrictedAreaFilterSet,
                            ZoningFilterSet, MapEntityFilterSet):
    bbox = PythonPolygonFilter(field_name='geom')
    name = CharFilter(label=_('Name'), lookup_expr='icontains')

    class Meta(MapEntityFilterSet.Meta):
        model = Intervention
        fields = MapEntityFilterSet.Meta.fields + [
            'name'
        ]
