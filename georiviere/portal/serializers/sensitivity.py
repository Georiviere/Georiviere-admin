from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometryField


from geotrek.sensitivity.models import SensitiveArea


class SensitivitySerializer(GeoFeatureModelSerializer):
    geometry = GeometryField(read_only=True, precision=7, source='geom_transformed')

    class Meta:
        model = SensitiveArea
        geo_field = 'geometry'
        id_field = False
        fields = ('id', 'species')
