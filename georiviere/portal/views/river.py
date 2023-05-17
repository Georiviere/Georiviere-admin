from georiviere.river.models import Stream
from django.conf import settings
from django.db.models import F
from django.contrib.gis.db.models.functions import Transform

from georiviere.portal.serializers.river import StreamGeojsonSerializer, StreamSerializer
from georiviere.main.renderers import GeoJSONRenderer

from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework import permissions as rest_permissions


class StreamViewSet(viewsets.ModelViewSet):
    model = Stream
    geojson_serializer_class = StreamGeojsonSerializer
    serializer_class = StreamSerializer
    renderer_classes = (JSONRenderer, GeoJSONRenderer, )
    permission_classes = [rest_permissions.DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        portal_pk = self.kwargs['portal_pk']
        queryset = Stream.objects.filter(portals__id=portal_pk)
        queryset = queryset.annotate(geom_transformed=Transform(F('geom'), settings.API_SRID))
        return queryset

    def get_serializer_class(self):
        """ Use specific Serializer for GeoJSON """
        renderer, media_type = self.perform_content_negotiation(self.request)
        if getattr(renderer, 'format') == 'geojson':
            return self.geojson_serializer_class
        return self.serializer_class
