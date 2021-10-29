from rest_framework.serializers import ModelSerializer
from rest_framework_gis.fields import GeometryField
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from georiviere.finances_administration.models import AdministrativeFile


class AdministrativeFileSerializer(ModelSerializer):
    class Meta:
        model = AdministrativeFile
        fields = (
            'id', 'name', 'description', 'begin_date', 'end_date',
            'adminfile_type', 'domain', 'constraints', 'global_cost',
            'contractors', 'project_owners', 'project_managers',
            'structure', 'date_insert', 'date_update',
        )


class AdministrativeFileGeojsonSerializer(GeoFeatureModelSerializer, AdministrativeFileSerializer):
    # Annotated geom field with API_SRID
    api_geom = GeometryField(read_only=True, precision=7)

    class Meta(AdministrativeFileSerializer.Meta):
        geo_field = 'api_geom'
        fields = AdministrativeFileSerializer.Meta.fields + ('api_geom', )
