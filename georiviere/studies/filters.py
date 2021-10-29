from django_filters import CharFilter
from django.utils.translation import gettext_lazy as _
from mapentity.filters import MapEntityFilterSet

from georiviere.studies.models import Study

from georiviere.watershed.filters import WatershedFilterSet

from geotrek.zoning.filters import ZoningFilterSet


class StudyFilterSet(WatershedFilterSet, ZoningFilterSet, MapEntityFilterSet):
    title = CharFilter(label=_('Title'), lookup_expr='icontains')
    start_year = CharFilter(label=_('Start year'), field_name='year', lookup_expr='gte')
    end_year = CharFilter(label=_('End year'), field_name='year', lookup_expr='lte')

    class Meta(MapEntityFilterSet.Meta):
        model = Study
        fields = MapEntityFilterSet.Meta.fields + ['title', 'study_types', 'start_year', 'end_year']
