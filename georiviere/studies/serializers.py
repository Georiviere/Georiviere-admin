from mapentity.registry import app_settings

from rest_framework.serializers import ModelSerializer
from rest_framework_gis.fields import GeometryField
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from georiviere.studies.models import Study


class StudySerializer(ModelSerializer):

    class Meta:
        model = Study
        fields = (
            'id', 'title', 'description'
        )


class StudyAPIGeojsonSerializer(GeoFeatureModelSerializer, StudySerializer):
    # Annotated geom field with API_SRID
    api_geom = GeometryField(read_only=True, precision=app_settings.get('GEOJSON_PRECISION'))

    class Meta(StudySerializer.Meta):
        geo_field = 'api_geom'
        fields = StudySerializer.Meta.fields + ('api_geom', )
