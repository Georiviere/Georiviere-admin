from rest_framework.permissions import AllowAny

from django.conf import settings
from django.db.models import F, Q
from django.contrib.gis.db.models.functions import Transform
from django.utils import translation

from djangorestframework_camel_case.render import CamelCaseJSONRenderer

from georiviere.contribution.models import Contribution
from georiviere.main.renderers import GeoJSONRenderer
from georiviere.portal.serializers.contribution import (ContributionSchemaSerializer,
                                                        ContributionSerializer, ContributionGeojsonSerializer)

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import renderers
from rest_framework.decorators import action
from rest_framework.response import Response


class ContributionViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    model = Contribution
    permission_classes = [AllowAny, ]
    geojson_serializer_class = ContributionGeojsonSerializer
    serializer_class = ContributionSerializer
    renderer_classes = [CamelCaseJSONRenderer, GeoJSONRenderer, ]

    @action(detail=False, url_name="json_schema", methods=['get'],
            renderer_classes=[renderers.JSONRenderer],
            serializer_class=ContributionSchemaSerializer)
    def json_schema(self, request, *args, **kwargs):
        serializer = self.get_serializer({})
        return Response(serializer.data)

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super().get_serializer_context()
        context['portal_pk'] = self.kwargs['portal_pk']
        translation.activate(self.kwargs['lang'])
        return context

    def get_queryset(self):
        portal_pk = self.kwargs['portal_pk']
        queryset = Contribution.objects.filter(portal_id=portal_pk, published=True)
        queryset = queryset.exclude(
            Q(potential_damage__isnull=True) & Q(fauna_flora__isnull=True) & Q(quantity__isnull=True)
            & Q(quality__isnull=True) & Q(landscape_element__isnull=True)
        )
        queryset = queryset.annotate(geom_transformed=Transform(F('geom'), settings.API_SRID))
        return queryset

    def get_serializer_class(self):
        """ Use specific Serializer for GeoJSON """
        renderer, media_type = self.perform_content_negotiation(self.request)
        if getattr(renderer, 'format') == 'geojson':
            return self.geojson_serializer_class
        return self.serializer_class
