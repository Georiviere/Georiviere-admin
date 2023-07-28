from django.conf import settings
from django.db.models import F
from django.contrib.gis.db.models.functions import Transform

from georiviere.portal.serializers.zoning import (CityGeojsonSerializer, DistrictGeojsonSerializer,
                                                  WatershedGeojsonSerializer)
from georiviere.main.renderers import GeoJSONRenderer
from geotrek.zoning.models import City, District
from georiviere.watershed.models import Watershed

from rest_framework import viewsets
from rest_framework.permissions import AllowAny


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CityGeojsonSerializer
    geojson_serializer_class = CityGeojsonSerializer
    permission_classes = [AllowAny, ]
    renderer_classes = [GeoJSONRenderer, ]

    def get_queryset(self):
        return City.objects.annotate(geom_transformed=Transform(F('geom'), settings.API_SRID))


@extend_schema_view(
    list=extend_schema(exclude=True),
    update=extend_schema(exclude=True),
    retrieve=extend_schema(exclude=True),
    create=extend_schema(exclude=True),
    destroy=extend_schema(exclude=True),
    partial_update=extend_schema(exclude=True),
)
class DistrictViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DistrictGeojsonSerializer
    geojson_serializer_class = DistrictGeojsonSerializer
    permission_classes = [AllowAny, ]
    renderer_classes = [GeoJSONRenderer, ]

    def get_queryset(self):
        return District.objects.annotate(geom_transformed=Transform(F('geom'), settings.API_SRID))


@extend_schema_view(
    list=extend_schema(exclude=True),
    update=extend_schema(exclude=True),
    retrieve=extend_schema(exclude=True),
    create=extend_schema(exclude=True),
    destroy=extend_schema(exclude=True),
    partial_update=extend_schema(exclude=True),
)
class WatershedViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = WatershedGeojsonSerializer
    geojson_serializer_class = WatershedGeojsonSerializer
    permission_classes = [AllowAny, ]
    renderer_classes = [GeoJSONRenderer, ]

    def get_queryset(self):
        return Watershed.objects.annotate(geom_transformed=Transform(F('geom'), settings.API_SRID))
