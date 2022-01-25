from django_filters import ModelMultipleChoiceFilter
from django.utils.translation import gettext_lazy as _
from mapentity.filters import MapEntityFilterSet
from geotrek.zoning.filters import ZoningFilterSet

from georiviere.proceeding.models import Proceeding, EventType
from georiviere.watershed.filters import WatershedFilterSet


class ProceedingFilterSet(WatershedFilterSet, ZoningFilterSet, MapEntityFilterSet):

    event_type = ModelMultipleChoiceFilter(
        method="filter_event_type",
        label=_("Related events type"),
        queryset=EventType.objects.all(),
    )

    class Meta(MapEntityFilterSet.Meta):
        model = Proceeding
        fields = MapEntityFilterSet.Meta.fields + ['name', 'date', 'event_type']

    def filter_event_type(self, qs, name, values):
        if not values:
            return qs
        return qs.filter(events__event_type__in=values)
