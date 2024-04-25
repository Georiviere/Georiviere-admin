import json
import logging
import os

from PIL import Image
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.db.models.functions import Transform
from django.core.exceptions import ValidationError
from django.core.files import File
from django.core.mail import send_mail
from django.db.models import F, Q
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from rest_framework import filters, viewsets, mixins, renderers, permissions, status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from georiviere.contribution.models import (
    Contribution,
    CustomContributionType,
    CustomContribution,
)
from georiviere.main.models import Attachment, FileType
from georiviere.main.renderers import GeoJSONRenderer
from georiviere.portal.serializers.contribution import (
    ContributionSchemaSerializer,
    ContributionSerializer,
    ContributionGeojsonSerializer,
    CustomContributionTypeSerializer,
    CustomContributionSerializer,
    CustomContributionGeoJSONSerializer,
)
from georiviere.portal.views.mixins import GeoriviereAPIMixin

logger = logging.getLogger(__name__)


class ContributionViewSet(
    GeoriviereAPIMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    model = Contribution
    geojson_serializer_class = ContributionGeojsonSerializer
    serializer_class = ContributionSerializer
    permission_classes = [
        AllowAny,
    ]
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    # TODO: Fix search filter with IntegerField (choices). It might be possible using an annotate on this view.
    # search_fields = ['potential_damage__type', 'fauna_flora__type', 'quality__type', 'quantity__type',
    #                  'landscape_element__type']

    @action(
        detail=False,
        url_name="json_schema",
        methods=["get"],
        renderer_classes=[renderers.JSONRenderer],
        serializer_class=ContributionSchemaSerializer,
    )
    def json_schema(self, request, *args, **kwargs):
        serializer = self.get_serializer({})
        return Response(serializer.data)

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super().get_serializer_context()
        translation.activate(self.kwargs["lang"])
        return context

    def get_queryset(self):
        portal_pk = self.kwargs["portal_pk"]
        queryset = Contribution.objects.filter(portal_id=portal_pk, published=True)
        queryset = queryset.exclude(
            Q(potential_damage__isnull=True)
            & Q(fauna_flora__isnull=True)
            & Q(quantity__isnull=True)
            & Q(quality__isnull=True)
            & Q(landscape_element__isnull=True)
        )
        queryset = queryset.annotate(
            geom_transformed=Transform(F("geom"), settings.API_SRID)
        )
        return queryset

    def create(self, request, *args, **kwargs):
        response = super().create(request)

        for file in request._request.FILES.values():
            attachment = Attachment(
                filetype=FileType.objects.get_or_create(
                    type=settings.CONTRIBUTION_FILETYPE
                )[0],
                content_type=ContentType.objects.get_for_model(Contribution),
                object_id=response.data.get("id"),
                attachment_file=file,
            )
            name, extension = os.path.splitext(file.name)
            try:
                attachment.full_clean()  # Check that file extension and mimetypes are allowed
            except ValidationError as e:
                logger.error(
                    f"Invalid attachment {name}{extension} for contribution {response.data.get('id')} : "
                    + str(e)
                )
            else:
                try:
                    # Reencode file to bitmap then back to jpeg lfor safety
                    if not os.path.exists(f"{settings.TMP_DIR}/contribution_file/"):
                        os.mkdir(f"{settings.TMP_DIR}/contribution_file/")
                    tmp_bmp_path = os.path.join(
                        f"{settings.TMP_DIR}/contribution_file/", f"{name}.bmp"
                    )
                    tmp_jpeg_path = os.path.join(
                        f"{settings.TMP_DIR}/contribution_file/", f"{name}.jpeg"
                    )
                    Image.open(file).save(tmp_bmp_path)
                    Image.open(tmp_bmp_path).save(tmp_jpeg_path)
                    with open(tmp_jpeg_path, "rb") as converted_file:
                        attachment.attachment_file = File(
                            converted_file, name=f"{name}.jpeg"
                        )
                        attachment.save()
                    os.remove(tmp_bmp_path)
                    os.remove(tmp_jpeg_path)
                except Exception as e:
                    logger.error(
                        f"Failed to convert attachment {name}{extension} for report {response.data.get('id')}: "
                        + str(e)
                    )
        if settings.SEND_REPORT_ACK and response.status_code == 201:
            send_mail(
                _("Georiviere : Contribution"),
                _(
                    """Hello,

                We acknowledge receipt of your contribution, thank you for your interest in Georiviere.

                Best regards,

                The Georiviere Team
                http://georiviere.fr"""
                ),
                settings.DEFAULT_FROM_EMAIL,
                [
                    json.loads(request.data.get("properties")).get("email_author"),
                ],
            )
        return response


class CustomContributionTypeViewSet(
    GeoriviereAPIMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = CustomContributionType.objects.all().prefetch_related(
        "stations", "fields"
    )
    serializer_class = CustomContributionTypeSerializer
    renderer_classes = (
        (
            renderers.BrowsableAPIRenderer,
            JSONRenderer,
        )
        if settings.DEBUG
        else (JSONRenderer,)
    )
    permission_classes = [permissions.AllowAny]
    pagination_class = LimitOffsetPagination

    def create_contribution(self, request, *args, **kwargs):
        context = self.get_serializer_context()
        custom_type = self.get_object()
        context["custom_type"] = custom_type
        serializer = self.get_serializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        extra_save_params = {}
        # if station selected, save its geom
        if "station" in serializer.validated_data:
            extra_save_params["geom"] = serializer.validated_data["station"].geom
        contribution = serializer.save(custom_type=custom_type, **extra_save_params)
        # reload with extra fields
        contribution = CustomContribution.objects.with_type_values(custom_type).get(
            pk=contribution.pk
        )
        return Response(
            CustomContributionSerializer(contribution, context=context).data,
            status=status.HTTP_201_CREATED,
        )

    def list_contributions(self, request, *args, **kwargs):
        custom_type = self.get_object()
        context = self.get_serializer_context()
        context["custom_type"] = custom_type
        qs = CustomContribution.objects.with_type_values(custom_type)

        renderer, media_type = self.perform_content_negotiation(self.request)
        if getattr(renderer, "format") == "geojson":
            self.geojson_serializer_class = (
                CustomContributionGeoJSONSerializer
            )
            qs = qs.annotate(geometry=Transform(F("geom"), settings.API_SRID))

        serializer = self.get_serializer(qs, context=context, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        url_name="custom-contributions",
        url_path="contributions",
        methods=["get", "post"],
        renderer_classes=[renderers.JSONRenderer, GeoJSONRenderer],
        serializer_class=CustomContributionSerializer,
    )
    def contributions(self, request, *args, **kwargs):
        if request.method == "GET":
            return self.list_contributions(request, *args, **kwargs)
        elif request.method == "POST":
            return self.create_contribution(request, *args, **kwargs)
