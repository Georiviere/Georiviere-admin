from django_filters import BooleanFilter, CharFilter, FilterSet, MultipleChoiceFilter, ModelMultipleChoiceFilter
from django.utils.translation import gettext_lazy as _
from mapentity.filters import MapEntityFilterSet
from geotrek.common.filters import OptionalRangeFilter
from geotrek.zoning.filters import ZoningFilterSet

from georiviere.portal.models import Portal
from georiviere.river.models import Stream
from georiviere.watershed.filters import WatershedFilterSet


class StreamFilterSet(WatershedFilterSet, ZoningFilterSet, MapEntityFilterSet):
    length = OptionalRangeFilter(field_name='length', label=_('Length'))
    name = CharFilter(label=_('Name'), lookup_expr='icontains')
    flow = MultipleChoiceFilter(
        label=_('Flow'),
        choices=Stream.FlowChoices.choices
    )
    portals = ModelMultipleChoiceFilter(
        method="filter_portal",
        label=_("Portals"),
        queryset=Portal.objects.all(),
    )

    class Meta(MapEntityFilterSet.Meta):
        model = Stream
        fields = MapEntityFilterSet.Meta.fields + ['name', 'length', 'flow', 'classification_water_policy']

    def filter_portal(self, qs, name, values):
        if not values:
            return qs
        return qs.prefetch_related('portals').filter(portals__name__in=values)


class TopologyFilterSet(FilterSet):
    qualified = BooleanFilter(label=_('Qualified'), field_name='topology__qualified')
