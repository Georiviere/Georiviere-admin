from collections import OrderedDict
from georiviere.api.valorization.serializers.map import MapBaseLayerSerializer, MapGroupLayerSerializer, MapLayerSerializer
from georiviere.portal.models import Portal

from rest_framework.serializers import ModelSerializer


class PortalSerializer(ModelSerializer):
    map = MapBaseLayerSerializer(many=True, source='map_base_layers')
    group = MapGroupLayerSerializer(many=True, source='mapgrouplayer_set')

    class Meta:
        model = Portal
        fields = (
            'id', 'name', 'map', 'group'
        )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['group'].append(
            OrderedDict({'label': None,
                         'layers': MapLayerSerializer(
                             instance.layers.filter(group_layer__isnull=True),
                             many=True,
                         ).data}))
        return ret
