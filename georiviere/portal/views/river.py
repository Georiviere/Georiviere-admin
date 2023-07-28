from georiviere.river.models import Stream
from django.conf import settings
from django.db.models import F
from django.contrib.gis.db.models.functions import Centroid, Transform

from georiviere.portal.serializers.river import StreamGeojsonSerializer, StreamSerializer
from georiviere.main.renderers import GeoJSONRenderer


from djangorestframework_camel_case.render import CamelCaseJSONRenderer

from rest_framework import filters, viewsets
from rest_framework import permissions as rest_permissions
from rest_framework.pagination import LimitOffsetPagination


class StreamViewSet(viewsets.ReadOnlyModelViewSet):
    model = Stream
    geojson_serializer_class = StreamGeojsonSerializer
    serializer_class = StreamSerializer
    renderer_classes = (CamelCaseJSONRenderer, GeoJSONRenderer, )
    permission_classes = [rest_permissions.DjangoModelPermissionsOrAnonReadOnly]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    pagination_class = LimitOffsetPagination
    ordering_fields = ['name', 'date_insert']
    search_fields = ['name']

    def get_queryset(self):
        portal_pk = self.kwargs['portal_pk']
        queryset = Stream.objects.filter(portals__id=portal_pk)
        queryset = queryset.annotate(geom_transformed=Transform(F('geom'), settings.API_SRID)).annotate(
            centroid=Centroid('geom_transformed'))
        return queryset

    def get_serializer_class(self):
        """ Use specific Serializer for GeoJSON """
        renderer, media_type = self.perform_content_negotiation(self.request)
        if getattr(renderer, 'format') == 'geojson':
            return self.geojson_serializer_class
        return self.serializer_class
