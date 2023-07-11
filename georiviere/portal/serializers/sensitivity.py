from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometryField

from georiviere.portal.serializers.main import AttachmentSerializer
from geotrek.sensitivity.models import SensitiveArea, Species


class SpeciesGeojsonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = ('id', 'pictogram', 'name')


class SensitivityGeojsonSerializer(GeoFeatureModelSerializer):
    geometry = GeometryField(read_only=True, precision=7, source='geom_transformed')
    species = SpeciesGeojsonSerializer(many=False)
    attachments = AttachmentSerializer(many=True)

    class Meta:
        model = SensitiveArea
        geo_field = 'geometry'
        id_field = False
        fields = ('id', 'attachments', 'description', 'species')


class SpeciesSerializer(serializers.ModelSerializer):
    period01 = serializers.BooleanField(read_only=True)
    period02 = serializers.BooleanField(read_only=True)
    period03 = serializers.BooleanField(read_only=True)
    period04 = serializers.BooleanField(read_only=True)
    period05 = serializers.BooleanField(read_only=True)
    period06 = serializers.BooleanField(read_only=True)
    period07 = serializers.BooleanField(read_only=True)
    period08 = serializers.BooleanField(read_only=True)
    period09 = serializers.BooleanField(read_only=True)
    period10 = serializers.BooleanField(read_only=True)
    period11 = serializers.BooleanField(read_only=True)
    period12 = serializers.BooleanField(read_only=True)
    url = serializers.URLField(read_only=True)

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
        fields = ('id', 'name', 'species', 'description', 'attachments')
