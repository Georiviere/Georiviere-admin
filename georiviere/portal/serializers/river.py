from georiviere.river.models import Stream
from georiviere.portal.serializers.main import AttachmentSerializer

from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework_gis import serializers as geo_serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class StreamGeojsonSerializer(GeoFeatureModelSerializer):
    geometry = geo_serializers.GeometryField(read_only=True, precision=7, source="geom_transformed")
    flow = SerializerMethodField()
    attachments = AttachmentSerializer(many=True)

    class Meta:
        model = Stream
        geo_field = 'geometry'
        id_field = False
        fields = (
            'id', 'name', 'description', 'length', 'descent', 'flow', 'attachments', 'geometry'
        )

    def get_flow(self, obj):
        return obj.get_flow_display()


class StreamSerializer(ModelSerializer):
    attachments = AttachmentSerializer(many=True)
    flow = SerializerMethodField()

    class Meta:
        model = Stream
        fields = (
            'id', 'name', 'description', 'length', 'descent', 'flow', 'attachments'
        )

    def get_flow(self, obj):
        return obj.get_flow_display()
