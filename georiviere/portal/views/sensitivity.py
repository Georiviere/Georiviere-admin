from django.conf import settings
from django.db.models import F
from django.contrib.gis.db.models.functions import Transform

from georiviere.portal.serializers.sensitivity import SensitivitySerializer
from georiviere.main.renderers import GeoJSONRenderer
from geotrek.sensitivity.models import SensitiveArea

from rest_framework import viewsets
from rest_framework.permissions import AllowAny


class SensitivityViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SensitivitySerializer
    permission_classes = [AllowAny, ]
    renderer_classes = [GeoJSONRenderer, ]

    def get_queryset(self):
        qs = SensitiveArea.objects.select_related('species').filter(published=True)
        qs = qs.annotate(geom_transformed=Transform(F('geom'),
                                                    settings.API_SRID))
        qs = qs.only('id', 'species')
        return qs
