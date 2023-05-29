from rest_framework.permissions import AllowAny

from djangorestframework_camel_case.render import CamelCaseJSONRenderer

from georiviere.contribution.models import Contribution

from georiviere.portal.serializers.contribution import ContributionSchemaSerializer, ContributionSerializer

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response


class ContributionViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    model = Contribution
    permission_classes = [AllowAny, ]
    serializer_class = ContributionSerializer
    renderer_classes = [CamelCaseJSONRenderer, ]

    @action(detail=False, url_name="contributions_schema", methods=['get'],
            renderer_classes=[CamelCaseJSONRenderer],
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
        return context
