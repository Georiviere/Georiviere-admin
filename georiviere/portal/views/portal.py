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

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super().get_serializer_context()
        context['portal_pk'] = self.kwargs['pk']
        return context
