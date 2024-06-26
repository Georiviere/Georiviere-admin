from django.conf import settings
from django.contrib.gis.db.models.functions import Centroid, Transform
from django.db.models import F, Prefetch
from rest_framework import filters, viewsets

from georiviere.main.models import Attachment
from georiviere.portal.filters import SearchNoAccentFilter
from georiviere.portal.serializers.river import (
    StreamGeojsonSerializer,
    StreamSerializer,
)
from georiviere.portal.views.mixins import GeoriviereAPIMixin
from georiviere.river.models import Stream


class StreamViewSet(GeoriviereAPIMixin, viewsets.ReadOnlyModelViewSet):
    model = Stream
    geojson_serializer_class = StreamGeojsonSerializer
    serializer_class = StreamSerializer
    filter_backends = [filters.OrderingFilter, SearchNoAccentFilter]

    ordering_fields = ["name", "date_insert"]
    search_fields = ["&name"]

    def get_model(self):
        return self.model

    def get_queryset(self):
        portal_pk = self.kwargs["portal_pk"]
        queryset = Stream.objects.filter(portals__id=portal_pk).prefetch_related(
            Prefetch(
                "attachments",
                queryset=Attachment.objects.all().select_related("filetype"),
            )
        )
        queryset = queryset.annotate(
            geom_transformed=Transform(F("geom"), settings.API_SRID)
        ).annotate(centroid=Centroid("geom_transformed"))
        return queryset

    def view_cache_key(self):
        return f"stream-{self.kwargs['portal_pk']}"
