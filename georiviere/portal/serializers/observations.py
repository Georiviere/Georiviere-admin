from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.serializers import ModelSerializer
from rest_framework_gis import serializers as geo_serializers

from georiviere.observations.models import Station
from georiviere.portal.serializers.mixins import SerializerAPIMixin


class StationMixin(SerializerAPIMixin, ModelSerializer):
    url = serializers.CharField(source="annex_uri")
    json_url = serializers.SerializerMethodField()
    geojson_url = serializers.SerializerMethodField()
    geometry = geo_serializers.GeometryField(
        read_only=True, precision=7, source="geom_transformed"
    )

    def get_json_url(self, obj):
        return reverse(
            "api_portal:stations-detail",
            kwargs=self._get_url_detail_kwargs(pk=obj.pk, format="json"),
        )

    def get_geojson_url(self, obj):
        return reverse(
            "api_portal:stations-detail",
            kwargs=self._get_url_detail_kwargs(pk=obj.pk, format="geojson"),
        )

    class Meta:
        model = Station
        fields = (
            "id",
            "code",
            "label",
            "description",
            "custom_contribution_types",
            "geometry",
            "url",
            "json_url",
            "geojson_url"
        )


class StationGeojsonSerializer(StationMixin, geo_serializers.GeoFeatureModelSerializer):
    class Meta(StationMixin.Meta):
        geo_field = "geometry"
        id_field = False


class StationSerializer(StationMixin, ModelSerializer):
    class Meta(StationMixin.Meta):
        pass
