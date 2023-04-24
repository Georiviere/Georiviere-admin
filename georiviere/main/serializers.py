from django.db import models as django_db_models

from rest_framework import serializers as rest_serializers
from rest_framework import serializers as rest_fields


class TranslatedModelSerializer(rest_serializers.ModelSerializer):
    def get_field(self, model_field):
        kwargs = {}
        if issubclass(model_field.__class__,
                      (django_db_models.CharField,
                       django_db_models.TextField)):
            if model_field.null:
                kwargs['allow_none'] = True
            kwargs['max_length'] = getattr(model_field, 'max_length')
            return rest_fields.CharField(**kwargs)
        return super().get_field(model_field)


class PictogramSerializerMixin(rest_serializers.ModelSerializer):
    pictogram = rest_serializers.ReadOnlyField(source='get_pictogram_url')
