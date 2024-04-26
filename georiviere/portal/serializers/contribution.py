from copy import deepcopy
from rest_framework import serializers
from rest_framework_gis import serializers as geo_serializers

from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry
from django.db import transaction
from django.db.models import ForeignKey
from django.utils.translation import gettext_lazy as _

from georiviere.contribution.schema import (
    get_contribution_properties,
    get_contribution_allOf,
    get_contribution_json_schema,
)
from georiviere.contribution.models import (
    Contribution,
    ContributionLandscapeElements,
    ContributionQuality,
    ContributionQuantity,
    ContributionFaunaFlora,
    ContributionPotentialDamage,
    SeverityType,
    CustomContributionType,
    CustomContribution,
)
from georiviere.portal.validators import validate_json_schema_data
from georiviere.portal.serializers.main import AttachmentSerializer


class ContributionGeojsonSerializer(geo_serializers.GeoFeatureModelSerializer):
    # Annotated geom field with API_SRID
    geometry = geo_serializers.GeometryField(
        read_only=True, precision=7, source="geom_transformed"
    )
    category = serializers.SerializerMethodField(read_only=True)

    class Meta:
        geo_field = "geometry"
        model = Contribution
        fields = ("id", "category", "geometry")

    def get_category(self, obj):
        return obj.category._meta.verbose_name.title()


class ContributionSerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(many=True, read_only=True)
    properties = serializers.JSONField(required=True, write_only=True)
    geom = geo_serializers.GeometryField(write_only=True)
    category = serializers.SerializerMethodField(read_only=True)
    type = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Contribution
        fields = (
            "id",
            "properties",
            "geom",
            "type",
            "category",
            "description",
            "attachments",
        )

    def get_category(self, obj):
        return obj.category._meta.verbose_name.title()

    def get_type(self, obj):
        return obj.category.get_type_display()

    def validate_properties(self, data):
        new_data = deepcopy(data)
        validate_json_schema_data(new_data, get_contribution_json_schema())
        return new_data

    def create(self, validated_data):
        sid = transaction.savepoint()
        msg = ""
        # Create a contribution depending on the data you get from the portal
        # The datas should follow the json schema generated in `georiviere/contribution/schema.py`
        # All the properties are flatten directly in the field properties
        # Properties depend on the category and type of contributions.
        # Check https://github.com/Georiviere/Georiviere-admin/issues/139
        # For more informations
        try:
            properties = validated_data.pop("properties")
            category = properties.pop("category")
            email_author = properties.pop("email_author")
            name_author = properties.pop("name_author", "")
            first_name_author = properties.pop("first_name_author", "")
            date_observation = properties.pop("date_observation")
            description = properties.pop("description", "")
            severity = properties.pop("severity", "")
            severity_instance = False
            if severity:
                severity_instance = SeverityType.objects.filter(label=severity)
            geom = validated_data.pop("geom")
            geom = GEOSGeometry(geom, srid=4326)
            geom = geom.transform(settings.SRID, clone=True)
            kwargs_contribution = {
                "geom": geom,
                "email_author": email_author,
                "date_observation": date_observation,
                "portal_id": self.context.get("portal_pk"),
                "name_author": name_author,
                "description": description,
                "first_name_author": first_name_author,
            }
            if bool(severity_instance):
                kwargs_contribution["severity"] = severity_instance.first()
            main_contribution = Contribution.objects.create(**kwargs_contribution)
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
                msg = _("Category is not valid")
                raise

            type_prop = properties.pop("type")
            # All the categories have a field type. We get all choices available and check
            # if the type exists for this category
            types = {v: k for k, v in model.TypeChoice.choices}
            for key, prop in properties.items():
                if isinstance(model._meta.get_field(key), ForeignKey):
                    properties[key] = model._meta.get_field(
                        key
                    ).related_model.objects.get(label=prop)
                    # If the type doesn't exist for this category, the error is catched, a validationerror occur.
            # If it exists, the contribution of the category in properties is created.
            model.objects.create(
                contribution=main_contribution, type=types[type_prop], **properties
            )
            transaction.savepoint_commit(sid)
        except Exception as e:
            transaction.savepoint_rollback(sid)
            if not msg:
                msg = f"{e.__class__.__name__} {e}"
            raise serializers.ValidationError({"Error": msg or _("An error occured")})
        return main_contribution


# Serializer for the contribution json schema's following the jsonschema reference :
# https://json-schema.org/understanding-json-schema/reference/conditionals.html
class ContributionSchemaSerializer(serializers.Serializer):
    type = serializers.CharField(default="object")
    required = serializers.SerializerMethodField(method_name="get_required")
    properties = serializers.SerializerMethodField()
    allOf = serializers.SerializerMethodField()

    def get_required(self, obj):
        # TODO: Loop on fields to get required
        return ["email_author", "date_observation", "category"]

    def get_properties(self, obj):
        return get_contribution_properties()

    def get_allOf(self, obj):
        return get_contribution_allOf()

    class Meta:
        geo_field = "geom"
        fields = ("type", "required", "properties", "allOf")


class CustomContributionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomContributionType
        fields = ("id", "label", "description", "json_schema_form", "stations")


class CustomContributionSerializer(serializers.ModelSerializer):
    contributed_at = serializers.DateTimeField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        custom_type = self.context.get("custom_type", None)
        if not custom_type:
            return

        # add and customize fields from json schema
        schema = custom_type.get_json_schema_form()
        for key in schema.get("properties", {}).keys():
            field = schema.get("properties", {}).get(key)
            output_field = serializers.CharField
            if field.get("type") == "number":
                output_field = serializers.FloatField
            elif field.get("type") == "integer":
                output_field = serializers.IntegerField
            elif field.get("type") == "boolean":
                output_field = serializers.BooleanField
            elif field.get("type") == "date":
                output_field = serializers.DateField
            elif field.get("type") == "datetime":
                output_field = serializers.DateTimeField
            # make field required or not
            self.fields[key] = output_field(
                label=field.get("title"), required=key in schema.get("required", [])
            )

        # station is required if defined at custom_type level. Geom is not required because replace by station geom
        if custom_type.stations.exists():
            self.fields["station"] = serializers.PrimaryKeyRelatedField(
                queryset=custom_type.stations.all(), required=True
            )
            self.fields["geom"].required = False

    def create(self, validated_data):
        custom_type = self.context.get("custom_type")
        # add and customize fields from json schema
        schema = custom_type.get_json_schema_form()

        data = {}
        for key, value in schema.get("properties").items():
            if key in validated_data:
                data[key] = validated_data.pop(key)
        validated_data["data"] = data
        return super().create(validated_data)

    class Meta:
        model = CustomContribution
        exclude = ("data", "custom_type", "validated")


class CustomContributionGeoJSONSerializer(
    CustomContributionSerializer,
    geo_serializers.GeoFeatureModelSerializer,
):
    geometry = geo_serializers.GeometryField(read_only=True, precision=7)
    geom = geo_serializers.GeometryField(write_only=True)

    class Meta(CustomContributionSerializer.Meta):
        geo_field = "geometry"
        exclude = ("data", "custom_type", "validated")


class CustomContributionByStationSerializer(serializers.ModelSerializer):
    class Meta(CustomContributionSerializer.Meta):
        model = CustomContribution
        exclude = ("data", "validated", "station", "portal")


class CustomContributionByStationGeoJSONSerializer(
    CustomContributionByStationSerializer,
    geo_serializers.GeoFeatureModelSerializer
):
    geometry = geo_serializers.GeometryField(read_only=True, precision=7)

    class Meta(CustomContributionByStationSerializer.Meta):
        geo_field = "geometry"
