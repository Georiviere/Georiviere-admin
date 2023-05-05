from django.conf import settings
from django.db.models import F
from django.contrib.gis.db.models.functions import Transform

from georiviere.api.valorization.serializers.valorization import POIGeojsonSerializer, POISerializer
from georiviere.main.renderers import GeoJSONRenderer
from georiviere.valorization.models import POI

from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework import renderers


class POIViewSet(viewsets.ReadOnlyModelViewSet):
    geojson_serializer_class = POIGeojsonSerializer
    serializer_class = POISerializer
    permission_classes = [AllowAny, ]
    renderer_classes = [renderers.JSONRenderer, GeoJSONRenderer]

    def get_queryset(self):
        queryset = POI.objects.select_related('type')
        queryset = queryset.annotate(geom_transformed=Transform(F('geom'), settings.API_SRID))
        return queryset

    def get_serializer_class(self):
        """ Use specific Serializer for GeoJSON """
        renderer, media_type = self.perform_content_negotiation(self.request)
        if getattr(renderer, 'format') == 'geojson':
            return self.geojson_serializer_class
        return self.serializer_class
