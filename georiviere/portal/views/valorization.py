from django.conf import settings
from django.db.models import F
from django.contrib.gis.db.models.functions import Transform
from django.shortcuts import get_object_or_404

from georiviere.portal.serializers.valorization import POIGeojsonSerializer, POISerializer
from georiviere.portal.views.mixins import GeoriviereAPIMixin
from georiviere.valorization.models import POI, POICategory

from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response


class POIViewSet(GeoriviereAPIMixin, viewsets.ReadOnlyModelViewSet):
    geojson_serializer_class = POIGeojsonSerializer
    serializer_class = POISerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['name', 'date_insert']
    search_fields = ['name', 'type__label', 'type__category__label']

    def get_queryset(self):
        portal_pk = self.kwargs['portal_pk']
        queryset = POI.objects.select_related('type')
        queryset = queryset.filter(portals__id=portal_pk).annotate(geom_transformed=Transform(F('geom'), settings.API_SRID))
        return queryset

    @action(detail=False, methods=['get'], permission_classes=[],
            url_path=r'category/(?P<category_pk>\d+)', url_name='category')
    def category(self, request, *args, **kwargs):
        category_pk = self.kwargs['category_pk']
        category = get_object_or_404(POICategory.objects.all(), pk=category_pk)
        qs = self.filter_queryset(POI.objects.filter(type__in=category.types.all()).annotate(
            geom_transformed=Transform(F('geom'), settings.API_SRID)))
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
