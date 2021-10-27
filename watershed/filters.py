from django_filters import FilterSet
from django.utils.translation import gettext_lazy as _


from .models import Watershed
from geotrek.zoning.filters import IntersectionFilter


class IntersectionFilterWatershed(IntersectionFilter):
    model = Watershed


class WatershedFilterSet(FilterSet):
    watershed = IntersectionFilterWatershed(label=_('Watershed'), required=False)
