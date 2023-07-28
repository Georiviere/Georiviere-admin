from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometryField

from georiviere.watershed.models import Watershed, WatershedType
from geotrek.zoning.models import City, District


class CityGeojsonSerializer(GeoFeatureModelSerializer):
    id = serializers.ReadOnlyField(source='code')
    geometry = GeometryField(read_only=True, precision=7, source='geom_transformed')

    class Meta:
        model = City
        geo_field = 'geometry'
        id_field = False
        fields = ('id', 'name')


class CitySerializer(GeoFeatureModelSerializer):
    id = serializers.ReadOnlyField(source='code')

    class Meta:
        model = City
        id_field = False
        fields = ('id', 'name')


class DistrictGeojsonSerializer(GeoFeatureModelSerializer):
    geometry = GeometryField(read_only=True, precision=7, source='geom_transformed')

    class Meta:
        model = District
        geo_field = 'geometry'
        id_field = False
        fields = ('id', 'name')


class DistrictSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = District
        id_field = False
        fields = ('id', 'name')


class WatershedTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatershedType
        fields = ("name", "color")


class WatershedGeojsonSerializer(GeoFeatureModelSerializer):
    type = WatershedTypeSerializer(source='watershed_type')
    geometry = GeometryField(read_only=True, precision=7, source='geom_transformed')

    class Meta:
        model = Watershed
        geo_field = 'geometry'
        id_field = False
        fields = ('id', 'name', 'type')


class WatershedSerializer(GeoFeatureModelSerializer):
    type = WatershedTypeSerializer(source='watershed_type')

    class Meta:
        model = Watershed
        id_field = False
        fields = ('id', 'name', 'type')
