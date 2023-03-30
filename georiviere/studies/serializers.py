from rest_framework.serializers import ModelSerializer
from rest_framework_gis.fields import GeometryField
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from georiviere.studies.models import Study


class StudySerializer(ModelSerializer):

    class Meta:
        model = Study
        fields = (
            'id', 'name', 'description'
        )


class StudyAPIGeojsonSerializer(GeoFeatureModelSerializer, StudySerializer):
    # Annotated geom field with API_SRID
    api_geom = GeometryField(read_only=True, precision=7)

    class Meta(StudySerializer.Meta):
        geo_field = 'api_geom'
        fields = StudySerializer.Meta.fields + ('api_geom', )
