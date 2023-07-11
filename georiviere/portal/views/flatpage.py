from rest_framework.permissions import AllowAny

from djangorestframework_camel_case.render import CamelCaseJSONRenderer

from georiviere.flatpages.models import FlatPage

from georiviere.portal.serializers.flatpage import FlatPageSerializer

from rest_framework import viewsets
from rest_framework import mixins


class FlatPageViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    model = FlatPage
    permission_classes = [AllowAny, ]
    serializer_class = FlatPageSerializer
    renderer_classes = [CamelCaseJSONRenderer, ]

    def get_queryset(self):
        portal_pk = self.kwargs['portal_pk']
        queryset = FlatPage.objects.filter(portals__in=[portal_pk])
        return queryset
