from django.conf import settings
from django.contrib.gis.db.models.functions import Centroid, Transform
from django.db.models import F, Prefetch
from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from rest_framework import filters, viewsets, permissions as rest_permissions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.renderers import BrowsableAPIRenderer

from georiviere.decorators import view_cache_response_content, view_cache_latest
from georiviere.main.models import Attachment
from georiviere.main.renderers import GeoJSONRenderer
from georiviere.portal.filters import SearchNoAccentFilter
from georiviere.portal.serializers.river import (
    StreamGeojsonSerializer,
    StreamSerializer,
)
from georiviere.river.models import Stream


class StreamViewSet(viewsets.ReadOnlyModelViewSet):
    model = Stream
    geojson_serializer_class = StreamGeojsonSerializer
    serializer_class = StreamSerializer
    renderer_classes = (
        BrowsableAPIRenderer,
        CamelCaseJSONRenderer,
        GeoJSONRenderer,
    )
    permission_classes = [rest_permissions.DjangoModelPermissionsOrAnonReadOnly]
    filter_backends = [filters.OrderingFilter, SearchNoAccentFilter]
    pagination_class = LimitOffsetPagination
    ordering_fields = ["name", "date_insert"]
    search_fields = ["&name"]

    def get_queryset(self):
        portal_pk = self.kwargs["portal_pk"]
        queryset = Stream.objects.filter(portals__id=portal_pk).prefetch_related(
            Prefetch("attachments",
                     queryset=Attachment.objects.all().select_related('filetype')))
        queryset = queryset.annotate(
            geom_transformed=Transform(F("geom"), settings.API_SRID)
        ).annotate(centroid=Centroid("geom_transformed"))
        return queryset

    def get_serializer_class(self):
        """Use specific Serializer for GeoJSON"""
        renderer, media_type = self.perform_content_negotiation(self.request)
        if getattr(renderer, "format") == "geojson":
            return self.geojson_serializer_class
        return self.serializer_class

    def view_cache_key(self):
        return f"stream-{self.kwargs['portal_pk']}"

    @view_cache_latest()
    @view_cache_response_content()
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
