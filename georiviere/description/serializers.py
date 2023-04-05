from mapentity.registry import app_settings

from rest_framework.serializers import ModelSerializer
from rest_framework_gis.fields import GeometryField
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from georiviere.description.models import Usage, UsageType


class UsageTypeSerialier(ModelSerializer):
    class Meta:
        model = UsageType
        fields = ('id', 'label')


class UsageSerializer(ModelSerializer):
    usage_types = UsageTypeSerialier(many=True)

    class Meta:
        model = Usage
        fields = (
            'id', 'name', 'usage_types', 'description'
        )


class UsageAPIGeojsonSerializer(GeoFeatureModelSerializer, UsageSerializer):
    # Annotated geom field with API_SRID
    api_geom = GeometryField(read_only=True, precision=app_settings.get('GEOJSON_PRECISION'))

    class Meta(UsageSerializer.Meta):
        geo_field = 'api_geom'
        fields = UsageSerializer.Meta.fields + ('api_geom', )
