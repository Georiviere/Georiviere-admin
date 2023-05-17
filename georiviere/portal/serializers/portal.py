from collections import OrderedDict
from georiviere.portal.serializers.map import MapBaseLayerSerializer, MapGroupLayerSerializer, MapLayerSerializer
from georiviere.portal.models import Portal

from django.conf import settings
from django.contrib.gis.geos import Polygon

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
            return obj.spatial_extent.transform(4326, clone=True).extent
        else:
            bbox = Polygon.from_bbox(settings.SPATIAL_EXTENT)
            bbox.srid = settings.SRID
            return bbox.transform(4326, clone=True).extent

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        layers_without_group = instance.layers.filter(group_layer__isnull=True)
        if layers_without_group.exists():
            ret['group'].append(
                OrderedDict({'label': None,
                             'layers': MapLayerSerializer(
                                 layers_without_group,
                                 many=True,
                             ).data}))
        return ret
