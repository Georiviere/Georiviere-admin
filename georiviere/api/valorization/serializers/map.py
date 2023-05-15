from georiviere.portal.models import MapBaseLayer, MapGroupLayer, MapLayer

from rest_framework.serializers import ModelSerializer, IntegerField, SerializerMethodField


class ControlLayerSerializer(ModelSerializer):
    minZoom = IntegerField(source='min_zoom')
    maxZoom = IntegerField(source='max_zoom')

    class Meta:
        model = MapBaseLayer
        fields = ('minZoom', 'maxZoom', 'attribution')


class MapLayerSerializer(ModelSerializer):
    options = SerializerMethodField()
    geojson_url = SerializerMethodField()
    url = SerializerMethodField()

    class Meta:
        model = MapLayer
        fields = (
            'id', 'label', 'default_active', 'options', 'geojson_url', 'url'
        )
        ordering = ('order',)

    def get_options(self, obj):
        return {'style': obj.style if obj.style else None}

    def get_geojson_url(self, obj):
        layer_type = obj.layer_type.split('-')
        prefix = ''
        if layer_type[0] in ['pois', 'streams']:
            prefix = f'{obj.portal.pk}/'
        if len(layer_type) == 2:
            filter_type = layer_type[-1]
            return f'{prefix}{layer_type[0]}/category/{filter_type}.geojson'
        return f'{prefix}{layer_type[0]}.geojson'

    def get_url(self, obj):
        layer_type = obj.layer_type.split('-')
        if layer_type[0] in ['pois', 'streams']:
            return f'{obj.portal.pk}/{layer_type[0]}'
        return None


class MapBaseLayerSerializer(ModelSerializer):
    control = ControlLayerSerializer(source='*')

    class Meta:
        model = MapBaseLayer
        fields = (
            'id', 'label', 'url', 'control',
        )
        ordering = ('order',)


class MapGroupLayerSerializer(ModelSerializer):
    layers = MapLayerSerializer(many=True)

    class Meta:
        model = MapGroupLayer
        fields = (
            'label', 'layers'
        )
