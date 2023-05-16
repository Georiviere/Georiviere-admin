from collections import OrderedDict
from georiviere.portal.serializers.map import MapBaseLayerSerializer, MapGroupLayerSerializer, MapLayerSerializer
from georiviere.portal.models import Portal

from django.conf import settings

from rest_framework.serializers import ModelSerializer, SerializerMethodField


class PortalSerializer(ModelSerializer):
    map = MapBaseLayerSerializer(many=True, source='map_base_layers')
    group = MapGroupLayerSerializer(many=True, source='mapgrouplayer_set')
    spatial_extent = SerializerMethodField()

    class Meta:
        model = Portal
        fields = (
            'id', 'name', 'map', 'group', 'spatial_extent'
        )

    def get_spatial_extent(self, obj):
        if obj.spatial_extent:
            return obj.spatial_extent.extent
        else:
            return settings.SPATIAL_EXTENT

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.layers.filter(group_layer__isnull=True).exists():
            ret['group'].append(
                OrderedDict({'label': None,
                             'layers': MapLayerSerializer(
                                 instance.layers.filter(group_layer__isnull=True),
                                 many=True,
                             ).data}))
        return ret
