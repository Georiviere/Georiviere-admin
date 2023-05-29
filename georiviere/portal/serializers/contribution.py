from copy import deepcopy
from rest_framework import serializers
from django.core.serializers.json import DjangoJSONEncoder

from georiviere.contribution.schema import (get_contribution_properties, get_contribution_allOf,
                                            get_contribution_json_schema)
from georiviere.contribution.models import (Contribution, ContributionLandscapeElements, ContributionQuality,
                                            ContributionQuantity, ContributionFaunaFlora, ContributionPotentialDamage)
from georiviere.portal.validators import validate_json_schema_data


class ContributionSerializer(serializers.ModelSerializer):
    properties = serializers.JSONField(required=True, encoder=DjangoJSONEncoder, write_only=True)

    class Meta:
        model = Contribution
        fields = (
            'properties', 'geom'
        )

    def validate_properties(self, data):
        new_data = deepcopy(data)
        validate_json_schema_data(new_data, get_contribution_json_schema())
        return new_data

    def create(self, validated_data):
        properties = validated_data.pop('properties')
        category = properties.pop('category')
        email_author = properties.pop('email_author')
        name_author = properties.pop('name_author', '')
        first_name_author = properties.pop('first_name_author', '')
        date_observation = properties.pop('date_observation')
        geom = validated_data.pop('geom')
        main_contribution = Contribution.objects.create(geom=geom, email_author=email_author,
                                                        date_observation=date_observation,
                                                        portal_id=self.context.get('portal_pk'),
                                                        name_author=name_author,
                                                        first_name_author=first_name_author)
        model = None

        if category == ContributionLandscapeElements._meta.verbose_name.title():
            model = ContributionLandscapeElements

        if category == ContributionQuality._meta.verbose_name.title():
            model = ContributionQuality

        if category == ContributionQuantity._meta.verbose_name.title():
            model = ContributionQuantity

        if category == ContributionPotentialDamage._meta.verbose_name.title():
            model = ContributionPotentialDamage

        if category == ContributionFaunaFlora._meta.verbose_name.title():
            model = ContributionFaunaFlora

        if not model:
            raise serializers.ValidationError({"category": "category is not valid"})

        type_prop = properties.pop('type')

        types = {v: k for k, v in model.TypeChoice.choices}

        contribution = model.objects.create(contribution=main_contribution,
                                            type=types[type_prop],
                                            **properties)

        return contribution

    def to_representation(self, instance):
        data = {
            'category': instance._meta.verbose_name.title(),
            'type': getattr(instance, 'type'),
            'email_author': instance.contribution.email_author,
            'name_author': instance.contribution.name_author,
            'first_name_author': instance.contribution.first_name_author,
            'date_observation': instance.contribution.date_observation,
        }
        return data


class ContributionSchemaSerializer(serializers.Serializer):
    type = serializers.CharField(default='object')
    required = serializers.SerializerMethodField(method_name='get_required')
    properties = serializers.SerializerMethodField()
    allOf = serializers.SerializerMethodField()

    def get_required(self, obj):
        # TODO: Loop on fields to get required
        return ['email_author', 'date_observation', 'category']

    def get_properties(self, obj):
        return get_contribution_properties()

    def get_allOf(self, obj):
        return get_contribution_allOf()

    class Meta:
        geo_field = 'geom'
        fields = (
            'type', 'required', 'properties', 'allOf'
        )
