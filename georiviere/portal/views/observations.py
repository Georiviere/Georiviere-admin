from django.conf import settings
from django.contrib.gis.db.models.functions import Transform
from django.db.models import F
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
        Station.objects.filter(custom_contribution_types__isnull=False).distinct('pk')  # filter station linked to custom contrib
        return Station.objects.all().annotate(geom_transformed=Transform(F("geom"), settings.API_SRID))
