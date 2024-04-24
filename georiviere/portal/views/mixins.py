from django.conf import settings
from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from rest_framework import renderers, permissions
from rest_framework.pagination import LimitOffsetPagination

from georiviere.main.renderers import GeoJSONRenderer


class GeoriviereAPIMixin:
    renderer_classes = (
        renderers.BrowsableAPIRenderer,
        CamelCaseJSONRenderer,
        GeoJSONRenderer,
    ) if settings.DEBUG else (CamelCaseJSONRenderer, GeoJSONRenderer)
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        """Use specific Serializer for GeoJSON"""
        renderer, media_type = self.perform_content_negotiation(self.request)
        if getattr(renderer, "format") == "geojson":
            return self.geojson_serializer_class
        return self.serializer_class

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["lang"] = self.kwargs["lang"]
        context["portal_pk"] = self.kwargs["portal_pk"]
        return context