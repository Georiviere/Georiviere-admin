from django_filters import BooleanFilter, CharFilter, FilterSet, MultipleChoiceFilter
from django.utils.translation import gettext_lazy as _
from mapentity.filters import MapEntityFilterSet
from geotrek.common.filters import OptionalRangeFilter
from geotrek.zoning.filters import ZoningFilterSet

from georiviere.river.models import Stream
from georiviere.watershed.filters import WatershedFilterSet


class StreamFilterSet(WatershedFilterSet, ZoningFilterSet, MapEntityFilterSet):
    length = OptionalRangeFilter(field_name='length', label=_('Length'))
    name = CharFilter(label=_('Name'), lookup_expr='icontains')
    flow = MultipleChoiceFilter(
        label=_('Flow'),
        choices=Stream.FlowChoices.choices
    )

    class Meta(MapEntityFilterSet.Meta):
        model = Stream
        fields = MapEntityFilterSet.Meta.fields + ['name', 'length', 'flow']


class TopologyFilterSet(FilterSet):
    qualified = BooleanFilter(label=_('Qualified'), field_name='topology__qualified')
