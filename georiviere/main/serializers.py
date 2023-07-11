from rest_framework import serializers as rest_serializers


class TranslatedModelSerializer(rest_serializers.ModelSerializer):
    pass


class PictogramSerializerMixin(rest_serializers.ModelSerializer):
    pictogram = rest_serializers.ReadOnlyField(source='get_pictogram_url')
