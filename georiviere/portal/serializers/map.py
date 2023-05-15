from django.urls import reverse

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
    json_schema_url = SerializerMethodField()
    url = SerializerMethodField()
    type = SerializerMethodField()
    is_searchable = SerializerMethodField()

    class Meta:
        model = MapLayer
        fields = (
            'id', 'label', 'default_active', 'options', 'geojson_url', 'json_schema_url', 'url', 'type', 'is_searchable'
        )
        ordering = ('order',)

    def get_is_searchable(self, obj):
        if obj.layer_type.split('-')[0] in ['pois', 'streams', 'contributions', 'sensitivities']:
            return True
        return False

    def get_options(self, obj):
        return {'style': obj.style if obj.style else None}

    def get_type(self, obj):
        return obj.layer_type.split('-')[0]

    def get_geojson_url(self, obj):
        layer_type = obj.layer_type.split('-')
        # TODO: Make lang dynamic
        reverse_kwargs = {'lang': 'fr', 'format': 'geojson'}
        if layer_type[0] in ['waterhseds', 'pois', 'streams', 'contributions']:
            reverse_kwargs['portal_pk'] = obj.portal.pk
        if len(layer_type) == 2:
            # If the layer type is poi, it's separated by category.
            filter_type = layer_type[-1]
            reverse_kwargs['category_pk'] = filter_type
            return reverse('api_portal:pois-category', kwargs=reverse_kwargs)
        return reverse(f'api_portal:{layer_type[0]}-list', kwargs=reverse_kwargs)

    def get_url(self, obj):
        layer_type = obj.layer_type.split('-')
        if layer_type[0] not in ['pois', 'streams', 'contributions', 'sensitivities']:
            return None
        # TODO: Make lang dynamic
        reverse_kwargs = {'lang': 'fr'}
        if layer_type[0] in ['waterhseds', 'pois', 'streams', 'contributions']:
            reverse_kwargs['portal_pk'] = obj.portal.pk
        return reverse(f'api_portal:{layer_type[0]}-list', kwargs=reverse_kwargs)

    def get_json_schema_url(self, obj):
        layer_type = obj.layer_type.split('-')
        # TODO: Make lang dynamic
        reverse_kwargs = {'lang': 'fr', 'portal_pk': obj.portal.pk}
        if layer_type[0] != 'contributions':
            return None
        return reverse(f'api_portal:{layer_type[0]}-json_schema', kwargs=reverse_kwargs)


class MapBaseLayerSerializer(ModelSerializer):
    control = ControlLayerSerializer(source='*')

    class Meta:
        model = MapBaseLayer
        fields = (
            'id', 'label', 'url', 'control',
        )
        ordering = ('order',)


class MapGroupLayerSerializer(ModelSerializer):
    layers = MapLayerSerializer(many=True, source='available_layers')

    class Meta:
        model = MapGroupLayer
        fields = (
            'label', 'layers'
        )
