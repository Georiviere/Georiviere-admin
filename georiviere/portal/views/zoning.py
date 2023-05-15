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

from djangorestframework_camel_case.render import CamelCaseJSONRenderer


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CitySerializer
    geojson_serializer_class = CityGeojsonSerializer
    permission_classes = [AllowAny, ]
    renderer_classes = [CamelCaseJSONRenderer, GeoJSONRenderer, ]

    def get_queryset(self):
        return City.objects.annotate(geom_transformed=Transform(F('geom'), settings.API_SRID))

    def get_serializer_class(self):
        """ Use specific Serializer for GeoJSON """
        renderer, media_type = self.perform_content_negotiation(self.request)
        if getattr(renderer, 'format') == 'geojson':
            return self.geojson_serializer_class
        return self.serializer_class


class DistrictViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DistrictSerializer
    geojson_serializer_class = DistrictGeojsonSerializer
    permission_classes = [AllowAny, ]
    renderer_classes = [CamelCaseJSONRenderer, GeoJSONRenderer, ]

    def get_queryset(self):
        return District.objects.annotate(geom_transformed=Transform(F('geom'), settings.API_SRID))

    def get_serializer_class(self):
        """ Use specific Serializer for GeoJSON """
        renderer, media_type = self.perform_content_negotiation(self.request)
        if getattr(renderer, 'format') == 'geojson':
            return self.geojson_serializer_class
        return self.serializer_class


class WatershedViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = WatershedSerializer
    geojson_serializer_class = WatershedGeojsonSerializer
    permission_classes = [AllowAny, ]
    renderer_classes = [CamelCaseJSONRenderer, GeoJSONRenderer, ]

    def get_queryset(self):
        portal_pk = self.kwargs['portal_pk']
        queryset = Watershed.objects.select_related('watershed_type').filter(watershed_type__portals__id=portal_pk)
        return queryset.annotate(geom_transformed=Transform(F('geom'), settings.API_SRID))

    def get_serializer_class(self):
        """ Use specific Serializer for GeoJSON """
        renderer, media_type = self.perform_content_negotiation(self.request)
        if getattr(renderer, 'format') == 'geojson':
            return self.geojson_serializer_class
        return self.serializer_class
