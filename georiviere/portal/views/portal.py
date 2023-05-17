from rest_framework.permissions import AllowAny

from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from georiviere.portal.models import Portal

from georiviere.portal.serializers.portal import PortalSerializer

from rest_framework import viewsets
from rest_framework import mixins


class PortalViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    model = Portal
    permission_classes = [AllowAny, ]
    serializer_class = PortalSerializer
    renderer_classes = [CamelCaseJSONRenderer, ]

    def get_queryset(self):
        return Portal.objects.all()
