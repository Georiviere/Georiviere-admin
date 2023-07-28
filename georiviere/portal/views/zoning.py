from django.conf import settings
from django.db.models import F
from django.contrib.gis.db.models.functions import Transform

from georiviere.portal.serializers.zoning import (CityGeojsonSerializer, DistrictGeojsonSerializer,
                                                  WatershedGeojsonSerializer, CitySerializer,
                                                  DistrictSerializer, WatershedSerializer)
from georiviere.main.renderers import GeoJSONRenderer
from geotrek.zoning.models import City, District
from georiviere.watershed.models import Watershed

from rest_framework import viewsets
from rest_framework.permissions import AllowAny


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CitySerializer
    geojson_serializer_class = CityGeojsonSerializer
    permission_classes = [AllowAny, ]
    renderer_classes = [GeoJSONRenderer, ]

    def get_queryset(self):
        return City.objects.annotate(geom_transformed=Transform(F('geom'), settings.API_SRID))


class DistrictViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DistrictSerializer
    geojson_serializer_class = DistrictGeojsonSerializer
    permission_classes = [AllowAny, ]
    renderer_classes = [GeoJSONRenderer, ]

    def get_queryset(self):
        return District.objects.annotate(geom_transformed=Transform(F('geom'), settings.API_SRID))


class WatershedViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = WatershedSerializer
    geojson_serializer_class = WatershedGeojsonSerializer
    permission_classes = [AllowAny, ]
    renderer_classes = [GeoJSONRenderer, ]

    def get_queryset(self):
        return Watershed.objects.annotate(geom_transformed=Transform(F('geom'), settings.API_SRID))
