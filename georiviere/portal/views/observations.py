from django.conf import settings
from django.db.models import Transform, F
from rest_framework import viewsets

from georiviere.observations.models import Station
from georiviere.portal.serializers.observations import (
    StationGeojsonSerializer,
    StationSerializer,
)
from georiviere.portal.views.mixins import GeoriviereAPIMixin


class StationViewSet(GeoriviereAPIMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = StationSerializer
    geojson_serializer_class = StationGeojsonSerializer

    def get_queryset(self):
        portal_pk = self.kwargs["portal_pk"]
        return (
            Station.objects.filter(custom_contribution_types__portal__id=portal_pk)
            .distinct()
            .annotate(geom_transformed=Transform(F("geom"), settings.API_SRID))
        )
