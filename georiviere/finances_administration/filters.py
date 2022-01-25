from django_filters import CharFilter
from django.utils.translation import gettext_lazy as _

from mapentity.filters import MapEntityFilterSet, PythonPolygonFilter
from geotrek.zoning.filters import ZoningFilterSet

from georiviere.finances_administration.models import AdministrativeFile
from georiviere.watershed.filters import WatershedFilterSet


class AdministrativeFileFilterSet(WatershedFilterSet, ZoningFilterSet, MapEntityFilterSet):
    bbox = PythonPolygonFilter(field_name='geom')
    name = CharFilter(label=_('Name'), lookup_expr='icontains')

    class Meta(MapEntityFilterSet.Meta):
        model = AdministrativeFile
        fields = MapEntityFilterSet.Meta.fields + [
            'name', 'adminfile_type', 'domain',
            'contractors', 'project_owners', 'project_managers', 'funders',
        ]
