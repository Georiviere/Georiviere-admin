from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometryField

from georiviere.watershed.models import Watershed
from geotrek.zoning.models import City, District


class CitySerializer(GeoFeatureModelSerializer):
    id = serializers.ReadOnlyField(source='code')
    geometry = GeometryField(read_only=True, precision=7, source='geom_transformed')

    class Meta:
        model = City
        geo_field = 'geometry'
        id_field = False
        fields = ('id', 'name')


class DistrictSerializer(GeoFeatureModelSerializer):
    id = serializers.ReadOnlyField(source='code')
    geometry = GeometryField(read_only=True, precision=7, source='geom_transformed')

    class Meta:
        model = District
        geo_field = 'geometry'
        id_field = False
        fields = ('id', 'name')


class WatershedSerializer(GeoFeatureModelSerializer):
    id = serializers.ReadOnlyField(source='code')
    geometry = GeometryField(read_only=True, precision=7, source='geom_transformed')

    class Meta:
        model = Watershed
        geo_field = 'geometry'
        id_field = False
        fields = ('id', 'name')
