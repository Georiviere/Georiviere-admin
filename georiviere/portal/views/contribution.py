from rest_framework.permissions import AllowAny

from djangorestframework_camel_case.render import CamelCaseJSONRenderer

from georiviere.contribution.models import Contribution

from georiviere.portal.serializers.contribution import ContributionSerializer

from rest_framework import viewsets
from rest_framework import mixins


class ContributionViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    model = Contribution
    permission_classes = [AllowAny, ]
    serializer_class = ContributionSerializer
    renderer_classes = [CamelCaseJSONRenderer, ]

    def get_queryset(self):
        return Contribution.objects.all()
