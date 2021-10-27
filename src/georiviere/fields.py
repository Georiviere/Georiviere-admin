from django.contrib.gis.geos import GEOSGeometry
from django.db.models import Field


class ElevationInfosField(Field):
    def db_type(self, connection):
        return 'elevation_infos'

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        final_value = value.replace('(', '').replace(')', '').split(',')
        return {
            'draped': GEOSGeometry(final_value[0]),
            'slope': float(final_value[1]),
            'min_elevation': int(final_value[2]),
            'max_elevation': int(final_value[3]),
            'positive_gain': int(final_value[4]),
            'negative_gain': int(final_value[5])
        }
