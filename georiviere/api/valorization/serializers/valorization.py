from georiviere.valorization.models import POI, POICategory, POIType
from georiviere.api.valorization.serializers.main import AttachmentSerializer

from rest_framework.serializers import ModelSerializer
from rest_framework_gis import serializers as geo_serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class POICategorySerializer(ModelSerializer):
    class Meta:
        model = POICategory
        fields = (
            'id', 'label'
        )


class POITypeSerializer(ModelSerializer):
    category = POICategorySerializer()

    class Meta:
        model = POIType
        fields = (
            'id', 'label', 'category', 'pictogram'
        )


class POIGeojsonSerializer(GeoFeatureModelSerializer):
    type = POITypeSerializer()
    geometry = geo_serializers.GeometryField(read_only=True, precision=7, source="geom_transformed")
    attachments = AttachmentSerializer(many=True)

    class Meta:
        model = POI
        geo_field = 'geometry'
        id_field = False
        fields = (
            'id', 'name', 'description', 'type', 'attachments', 'geometry'
        )


class POISerializer(ModelSerializer):
    type = POITypeSerializer()
    attachments = AttachmentSerializer(many=True)

    class Meta:
        model = POI
        fields = (
            'id', 'name', 'description', 'type', 'attachments'
        )
