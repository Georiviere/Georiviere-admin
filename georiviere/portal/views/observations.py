from django.conf import settings
from django.contrib.gis.db.models.functions import Transform
from django.db.models import F
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from georiviere.contribution.models import CustomContribution
from georiviere.observations.models import Station
from georiviere.portal.serializers.contribution import CustomContributionByStationSerializer, \
    CustomContributionByStationGeoJSONSerializer
from georiviere.portal.serializers.observations import (
    StationGeojsonSerializer,
    StationSerializer,
)
from georiviere.portal.views.mixins import GeoriviereAPIMixin


class StationViewSet(GeoriviereAPIMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = StationSerializer
    geojson_serializer_class = StationGeojsonSerializer

    def get_queryset(self):
        qs = Station.objects.filter(custom_contribution_types__isnull=False).distinct(
            "pk"
        )  # filter station linked to custom contrib
        return qs.annotate(geom_transformed=Transform(F("geom"), settings.API_SRID))

    @action(detail=True, methods=["get"],
            url_path=r"type/(?P<type_pk>\d+)/custom-contributions", url_name='custom-contributions',
            serializer_class=CustomContributionByStationSerializer)
    def custom_contributions(self, request, *args, **kwargs):
        station = self.get_object()
        custom_type = get_object_or_404(station.custom_contribution_types.all(), pk=kwargs["type_pk"])
        context = self.get_serializer_context()
        context["custom_type"] = custom_type
        qs = CustomContribution.objects.with_type_values(custom_type).filter(station=station, validated=True)
        renderer, media_type = self.perform_content_negotiation(self.request)
        if getattr(renderer, "format") == "geojson":
            self.geojson_serializer_class = CustomContributionByStationGeoJSONSerializer
            qs = qs.annotate(geometry=Transform(F("geom"), settings.API_SRID))

        serializer = self.get_serializer(qs, context=context, many=True)
        return Response(serializer.data)
