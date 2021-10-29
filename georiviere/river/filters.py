from django_filters import BooleanFilter, CharFilter, FilterSet
from django.utils.translation import gettext_lazy as _
from mapentity.filters import MapEntityFilterSet

from georiviere.main.filters import RestrictedAreaFilterSet
from georiviere.river.models import Stream
from georiviere.watershed.filters import WatershedFilterSet

from geotrek.common.filters import OptionalRangeFilter
from geotrek.zoning.filters import ZoningFilterSet


class StreamFilterSet(WatershedFilterSet, RestrictedAreaFilterSet, ZoningFilterSet, MapEntityFilterSet):
    length = OptionalRangeFilter(field_name='length', label=_('Length'))
    name = CharFilter(label=_('Name'), lookup_expr='icontains')

    class Meta(MapEntityFilterSet.Meta):
        model = Stream
        fields = MapEntityFilterSet.Meta.fields + ['name', 'length']


class TopologyFilterSet(FilterSet):
    qualified = BooleanFilter(label=_('Qualified'), field_name='topology__qualified')
