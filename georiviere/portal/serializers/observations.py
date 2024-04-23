from rest_framework.serializers import ModelSerializer
from rest_framework_gis import serializers as geo_serializers

from georiviere.observations.models import Station


class StationGeojsonSerializer(geo_serializers.GeoFeatureModelSerializer):
    geometry = geo_serializers.GeometryField(
        read_only=True, precision=7, source="geom_transformed"
    )

    class Meta:
        model = Station
        geo_field = "geometry"
        id_field = False
        fields = (
            "id",
            "code",
            "label",
            "description",
            "custom_contribution_types",
            "geometry",
        )


class StationSerializer(ModelSerializer):
    geometry = geo_serializers.GeometryField(
        read_only=True, precision=7, source="geom_transformed"
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
        )
