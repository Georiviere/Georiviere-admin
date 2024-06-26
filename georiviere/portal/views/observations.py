from django.conf import settings
from django.contrib.gis.db.models.functions import Transform
from django.db.models import F
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from georiviere.observations.models import Station
from georiviere.portal.serializers.contribution import (
    CustomContributionByStationSerializer,
)
from georiviere.portal.serializers.observations import (
    StationGeojsonSerializer,
    StationSerializer,
)
from georiviere.portal.views.mixins import GeoriviereAPIMixin


class StationViewSet(GeoriviereAPIMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = StationSerializer
    geojson_serializer_class = StationGeojsonSerializer

    def get_queryset(self):
        qs = Station.objects.filter(custom_contribution_types__isnull=False)
        return qs.annotate(geom_transformed=Transform(F("geom"), settings.API_SRID))

    @action(
        detail=True,
        methods=["get"],
        url_name="custom-contributions",
        serializer_class=CustomContributionByStationSerializer,
    )
    def custom_contributions(self, request, *args, **kwargs):
        station = self.get_object()
        qs = (
            station.custom_contributions.filter(validated=True)
            .prefetch_related("attachments")
            .defer(*CustomContributionByStationSerializer.Meta.exclude)
        )
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
