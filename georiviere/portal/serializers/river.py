from rest_framework import serializers
from rest_framework.reverse import reverse

from georiviere.portal.serializers.mixins import SerializerAPIMixin
from georiviere.river.models import Stream
from georiviere.portal.serializers.main import AttachmentSerializer

from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework_gis import serializers as geo_serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class StreamMixin(SerializerAPIMixin, ModelSerializer):
    flow = SerializerMethodField()
    attachments = AttachmentSerializer(many=True)
    json_url = serializers.SerializerMethodField()
    geojson_url = serializers.SerializerMethodField()

    def get_flow(self, obj):
        return obj.get_flow_display()

    def get_json_url(self, obj):
        return reverse(
            "api_portal:streams-detail",
            kwargs=self._get_url_detail_kwargs(pk=obj.pk, format="json"),
        )

    def get_geojson_url(self, obj):
        return reverse(
            "api_portal:streams-detail",
            kwargs=self._get_url_detail_kwargs(pk=obj.pk, format="geojson"),
        )

    class Meta:
        model = Stream
        fields = (
            "id",
            "name",
            "description",
            "length",
            "descent",
            "flow",
            "attachments",
            "json_url",
            "geojson_url",
        )


class StreamGeojsonSerializer(StreamMixin, GeoFeatureModelSerializer):
    geometry = geo_serializers.GeometryField(
        read_only=True, precision=7, source="geom_transformed"
    )

    class Meta(StreamMixin.Meta):
        geo_field = "geometry"
        id_field = False
        fields = StreamMixin.Meta.fields + ("geometry",)


class StreamSerializer(StreamMixin, ModelSerializer):
    geometry_center = geo_serializers.GeometryField(
        read_only=True, precision=7, source="centroid"
    )

    class Meta(StreamMixin.Meta):
        fields = StreamMixin.Meta.fields + ("geometry_center",)
