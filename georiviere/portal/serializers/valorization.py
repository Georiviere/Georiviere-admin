from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.serializers import ModelSerializer
from rest_framework_gis import serializers as geo_serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from georiviere.portal.serializers.main import AttachmentSerializer
from georiviere.portal.serializers.mixins import SerializerAPIMixin
from georiviere.valorization.models import POI, POICategory, POIType


class POICategorySerializer(ModelSerializer):
    class Meta:
        model = POICategory
        fields = ("id", "label")


class POITypeSerializer(ModelSerializer):
    category = POICategorySerializer()

    class Meta:
        model = POIType
        fields = ("id", "label", "category", "pictogram")


class POIMixin(SerializerAPIMixin, ModelSerializer):
    attachments = AttachmentSerializer(many=True)
    type = POITypeSerializer()
    json_url = serializers.SerializerMethodField()
    geojson_url = serializers.SerializerMethodField()

    def get_json_url(self, obj):
        return reverse(
            "api_portal:pois-detail",
            kwargs=self._get_url_detail_kwargs(pk=obj.pk, format="json"),
        )

    def get_geojson_url(self, obj):
        return reverse(
            "api_portal:pois-detail",
            kwargs=self._get_url_detail_kwargs(pk=obj.pk, format="geojson"),
        )

    class Meta:
        model = POI
        fields = (
            "id",
            "name",
            "description",
            "type",
            "attachments",
            "json_url",
            "geojson_url",
        )


class POIGeojsonSerializer(POIMixin, GeoFeatureModelSerializer):
    geometry = geo_serializers.GeometryField(
        read_only=True, precision=7, source="geom_transformed"
    )

    class Meta(POIMixin.Meta):
        geo_field = "geometry"
        id_field = False
        fields = POIMixin.Meta.fields + (
            "geometry",
        )


class POISerializer(POIMixin, ModelSerializer):
    class Meta(POIMixin.Meta):
        pass
