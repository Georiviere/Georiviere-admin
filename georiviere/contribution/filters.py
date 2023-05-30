from django_filters import CharFilter
from django.utils.translation import gettext_lazy as _
from mapentity.filters import MapEntityFilterSet, PythonPolygonFilter
from geotrek.zoning.filters import ZoningFilterSet

from georiviere.contribution.models import Contribution
from georiviere.watershed.filters import WatershedFilterSet


class ContributionFilterSet(WatershedFilterSet, ZoningFilterSet, MapEntityFilterSet):
    bbox = PythonPolygonFilter(field_name='geom')
    name_author = CharFilter(label=_('Name author'), lookup_expr='icontains')

    class Meta(MapEntityFilterSet.Meta):
        model = Contribution
        fields = MapEntityFilterSet.Meta.fields + [
            'name_author',
        ]
