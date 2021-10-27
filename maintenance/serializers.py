from rest_framework.serializers import ModelSerializer
from rest_framework_gis.fields import GeometryField
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from maintenance.models import Intervention


class InterventionSerializer(ModelSerializer):
    class Meta:
        model = Intervention
        fields = (
            'id', 'name', 'description',
            'intervention_status', 'intervention_type',
            'stake', 'disorders',
            'width', 'height',
        )


class InterventionGeojsonSerializer(GeoFeatureModelSerializer, InterventionSerializer):
    # Annotated geom field with API_SRID
    api_geom = GeometryField(read_only=True, precision=7)

    class Meta(InterventionSerializer.Meta):
        geo_field = 'api_geom'
        fields = InterventionSerializer.Meta.fields + ('api_geom', )
