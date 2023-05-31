from django.conf import settings
from django.db.models import F
from django.contrib.gis.db.models.functions import Transform

from djangorestframework_camel_case.render import CamelCaseJSONRenderer

from georiviere.portal.serializers.sensitivity import SensitivityGeojsonSerializer, SensitivitySerializer
from georiviere.main.renderers import GeoJSONRenderer
from geotrek.sensitivity.models import SensitiveArea

from rest_framework import viewsets
from rest_framework.permissions import AllowAny


class SensitivityViewSet(viewsets.ModelViewSet):
    model = SensitiveArea
    geojson_serializer_class = SensitivityGeojsonSerializer
    serializer_class = SensitivitySerializer
    permission_classes = [AllowAny, ]
    renderer_classes = [CamelCaseJSONRenderer, GeoJSONRenderer, ]

    def get_queryset(self):
        qs = SensitiveArea.objects.select_related('species').filter(published=True)
        qs = qs.annotate(geom_transformed=Transform(F('geom'),
                                                    settings.API_SRID))
        qs = qs.only('id', 'species')
        return qs

    def get_serializer_class(self):
        """ Use specific Serializer for GeoJSON """
        renderer, media_type = self.perform_content_negotiation(self.request)
        if getattr(renderer, 'format') == 'geojson':
            return self.geojson_serializer_class
        return self.serializer_class
