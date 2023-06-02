from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometryField

from georiviere.portal.serializers.main import AttachmentSerializer
from geotrek.sensitivity.models import SensitiveArea


class SensitivityGeojsonSerializer(GeoFeatureModelSerializer):
    geometry = GeometryField(read_only=True, precision=7, source='geom_transformed')

    class Meta:
        model = SensitiveArea
        geo_field = 'geometry'
        id_field = False
        fields = ('id', 'species')


class SensitivitySerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(many=True)
    name = serializers.CharField(source='species.name')

    class Meta:
        model = SensitiveArea
        fields = ('id', 'name', 'description', 'attachments')
