from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometryField

from georiviere.portal.serializers.main import AttachmentSerializer
from geotrek.sensitivity.models import SensitiveArea, Species


class SpeciesGeojsonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = ('id', 'pictogram', 'name', 'url')


class SensitivityGeojsonSerializer(GeoFeatureModelSerializer):
    geometry = GeometryField(read_only=True, precision=7, source='geom_transformed')
    name = serializers.CharField(source='species.name')
    species = SpeciesGeojsonSerializer()
    attachments = AttachmentSerializer(many=True)

    class Meta:
        model = SensitiveArea
        geo_field = 'geometry'
        id_field = False
        fields = ('id', 'attachments', 'description', 'species', 'name', 'contact')


class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = (
            'id', 'period01', 'period02', 'period03', 'period04', 'period05', 'period06', 'period07',
            'period08', 'period09', 'period10', 'period11', 'period12', 'url', 'pictogram'
        )


class SensitivitySerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(many=True)
    name = serializers.CharField(source='species.name')
    species = SpeciesSerializer(many=False)

    class Meta:
        model = SensitiveArea
        fields = ('id', 'name', 'species', 'description', 'attachments', 'contact')
