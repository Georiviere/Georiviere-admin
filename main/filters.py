from django_filters import FilterSet
from django.utils.translation import gettext_lazy as _

from geotrek.zoning.filters import IntersectionFilter
from geotrek.zoning.models import RestrictedArea


class IntersectionFilterRestrictedArea(IntersectionFilter):
    model = RestrictedArea


class RestrictedAreaFilterSet(FilterSet):
    restricted_area = IntersectionFilterRestrictedArea(label=_('Restricted area'), required=False)
