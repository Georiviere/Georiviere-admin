from drf_dynamic_fields import DynamicFieldsMixin
from rest_framework import serializers as rest_serializers

from mapentity.serializers import MapentityGeojsonModelSerializer
from georiviere.river import models as river_models


class StreamSerializer(DynamicFieldsMixin, rest_serializers.ModelSerializer):
    name = rest_serializers.CharField(source='name_display')
    structure = rest_serializers.SlugRelatedField('name', read_only=True)

    class Meta:
        model = river_models.Stream
        fields = "__all__"


class StreamGeojsonSerializer(MapentityGeojsonModelSerializer):
    class Meta(MapentityGeojsonModelSerializer.Meta):
        model = river_models.Stream
        fields = ('id', 'name')
