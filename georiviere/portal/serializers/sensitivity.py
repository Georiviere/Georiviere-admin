from geotrek.sensitivity.models import SensitiveArea, Species
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometryField

from georiviere.portal.serializers.main import AttachmentSerializer


class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = (
            'id', 'name', 'period01', 'period02', 'period03', 'period04', 'period05', 'period06', 'period07',
            'period08', 'period09', 'period10', 'period11', 'period12', 'url', 'pictogram'
        )


class SensitivitySerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(many=True)
    name = serializers.CharField(source='species.name')
    species = SpeciesSerializer()

    class Meta:
        model = SensitiveArea
        fields = ('id', 'name', 'species', 'description', 'attachments', 'contact')


class SensitivityGeojsonSerializer(GeoFeatureModelSerializer, SensitivitySerializer):
    geometry = GeometryField(read_only=True, precision=7, source='geom_transformed')

    class Meta(SensitivitySerializer.Meta):
        geo_field = 'geometry'
        id_field = False
