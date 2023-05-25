from rest_framework.permissions import AllowAny

from djangorestframework_camel_case.render import CamelCaseJSONRenderer

from georiviere.contribution.models import Contribution

from georiviere.portal.serializers.contribution import ContributionSerializer

from rest_framework import viewsets
from rest_framework import mixins


class ContributionViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    model = Contribution
    permission_classes = [AllowAny, ]
    serializer_class = ContributionSerializer
    renderer_classes = [CamelCaseJSONRenderer, ]

    def get_queryset(self):
        return Contribution.objects.all()

    def post(self, request, *args, **kwargs):
        return

    def get_serializer_class(self):
        """ Use specific Serializer for GeoJSON """
        return self.serializer_class
