from rest_framework.serializers import ModelSerializer
from rest_framework_gis.fields import GeometryField
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from knowledge.models import FollowUp


class FollowUpSerializer(ModelSerializer):
    class Meta:
        model = FollowUp
        fields = (
            'id', 'name', 'description', 'followup_type',
            'length', 'width', 'height',
        )


class FollowUpGeojsonSerializer(GeoFeatureModelSerializer, FollowUpSerializer):
    # Annotated geom field with API_SRID
    api_geom = GeometryField(read_only=True, precision=7)

    class Meta(FollowUpSerializer.Meta):
        geo_field = 'api_geom'
        fields = FollowUpSerializer.Meta.fields + ('api_geom', )
