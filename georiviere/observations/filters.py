from django_filters import ChoiceFilter, CharFilter, ModelMultipleChoiceFilter
from django.utils.translation import gettext_lazy as _
from mapentity.filters import MapEntityFilterSet
from geotrek.zoning.filters import ZoningFilterSet

from georiviere.watershed.filters import WatershedFilterSet
from georiviere.observations.models import Station, Parameter

choices = (
    (True, _("Yes")),
    (False, _("No"))
)


class StationFilterSet(WatershedFilterSet, ZoningFilterSet, MapEntityFilterSet):
    label = CharFilter(label=_('Label'), lookup_expr='icontains')
    code = CharFilter(label=_('Code'), lookup_expr='icontains')
    parameters_tracked = ModelMultipleChoiceFilter(
        method="filter_parameter",
        label=_("Tracked parameters"),
        queryset=Parameter.objects.all(),
    )
    in_service = ChoiceFilter(
        empty_label=_('In service'),
        null_label=_('Unknown'),
        choices=choices
    )

    class Meta(MapEntityFilterSet.Meta):
        model = Station
        fields = MapEntityFilterSet.Meta.fields + [
            'code', 'label', 'in_service',
            'station_profiles', 'parameters_tracked'
        ]

    def filter_parameter(self, qs, name, values):
        if not values:
            return qs
        return qs.filter(parametertracking__parameter__in=values)
