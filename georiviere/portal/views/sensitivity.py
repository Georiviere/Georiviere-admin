from django.conf import settings
from django.db.models import F, Case, Prefetch, When
from django.contrib.gis.db.models.functions import Transform

from djangorestframework_camel_case.render import CamelCaseJSONRenderer

from georiviere.functions import Area, Buffer, GeometryType
from georiviere.portal.serializers.sensitivity import SensitivityGeojsonSerializer, SensitivitySerializer
from georiviere.main.models import Attachment
from georiviere.main.renderers import GeoJSONRenderer
from geotrek.sensitivity.models import SensitiveArea

from rest_framework import filters
from rest_framework import viewsets
from rest_framework.permissions import AllowAny


class SensitivityViewSet(viewsets.ModelViewSet):
    model = SensitiveArea
    geojson_serializer_class = SensitivityGeojsonSerializer
    serializer_class = SensitivitySerializer
    permission_classes = [AllowAny, ]
    renderer_classes = [CamelCaseJSONRenderer, GeoJSONRenderer, ]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['species__name', ]
    search_fields = ['species__name', ]

    def get_queryset(self):
        queryset = (
            SensitiveArea.objects.existing()
            .filter(published=True)
            .select_related('species')
            .prefetch_related(
                'species__practices',
                Prefetch('attachments',
                         queryset=Attachment.objects.select_related('filetype')
                         )
            )
            .annotate(geom_type=GeometryType(F('geom')))
        )

        queryset = queryset.annotate(geom_transformed=Case(
            When(geom_type='POINT', then=Transform(Buffer(F('geom'), F('species__radius'), 4), settings.API_SRID)),
            default=Transform(F('geom'), settings.API_SRID)
        ))
        queryset = queryset.order_by(Area('geom_transformed').desc(), 'pk')
        if self.format_kwarg == 'geojson':
            queryset = queryset.only('id', 'species', 'attachments', 'description')
        return queryset.defer('geom')

    def get_serializer_class(self):
        """ Use specific Serializer for GeoJSON """
        renderer, media_type = self.perform_content_negotiation(self.request)
        if getattr(renderer, 'format') == 'geojson':
            return self.geojson_serializer_class
        return self.serializer_class
