from django.conf import settings
from django.db.models import F
from django.contrib.gis.db.models.functions import Transform
from django.shortcuts import get_object_or_404

from georiviere.portal.serializers.valorization import POIGeojsonSerializer, POISerializer
from georiviere.main.renderers import GeoJSONRenderer
from georiviere.valorization.models import POI, POICategory

from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response


from djangorestframework_camel_case.render import CamelCaseJSONRenderer


class POIViewSet(viewsets.ReadOnlyModelViewSet):
    geojson_serializer_class = POIGeojsonSerializer
    serializer_class = POISerializer
    permission_classes = [AllowAny, ]
    renderer_classes = [CamelCaseJSONRenderer, GeoJSONRenderer]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['name', 'date_insert']
    search_fields = ['name', 'type__label', 'type__category__label']

    def get_queryset(self):
        portal_pk = self.kwargs['portal_pk']
        queryset = POI.objects.select_related('type')
        queryset = queryset.filter(portals__id=portal_pk).annotate(geom_transformed=Transform(F('geom'), settings.API_SRID))
        return queryset

    def get_serializer_class(self):
        """ Use specific Serializer for GeoJSON """
        renderer, media_type = self.perform_content_negotiation(self.request)
        if getattr(renderer, 'format') == 'geojson':
            return self.geojson_serializer_class
        return self.serializer_class

    @action(detail=False, methods=['get'], permission_classes=[],
            url_path=r'category/(?P<category_pk>\d+)', url_name='category')
    def category(self, request, *args, **kwargs):
        category_pk = self.kwargs['category_pk']
        category = get_object_or_404(POICategory.objects.all(), pk=category_pk)
        qs = POI.objects.filter(type__in=category.types.select_related('pois').values_list('pk', flat=True)).annotate(
            geom_transformed=Transform(F('geom'), settings.API_SRID))
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
