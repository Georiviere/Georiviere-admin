from django.shortcuts import get_object_or_404
from djgeojson.views import GeoJSONLayerView

from geotrek.zoning.views import LandLayerMixin
from .models import Watershed, WatershedType


class WatershedGeoJSONLayer(LandLayerMixin, GeoJSONLayerView):
    model = Watershed
    properties = ['name']


class WatershedTypesGeoJSONLayer(LandLayerMixin, GeoJSONLayerView):
    model = Watershed

    def get_queryset(self):
        type_pk = self.kwargs['type_pk']
        qs = super().get_queryset().select_related('watershed_type')
        get_object_or_404(WatershedType, pk=type_pk)
        return qs.filter(watershed_type=type_pk)
