from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.gis.geos import GEOSGeometry, LineString,Point, Polygon
from django.conf import settings

from georiviere.river.fields import SnappedGeometryField, SnappedLineStringField
from georiviere.river.tests.factories import StreamFactory


class SnappedLineStringFieldTest(TestCase):
    def setUp(self):
        self.f = SnappedLineStringField()
        self.wktgeom = ('LINESTRING(-0.77054223313507 -5.32573853776343,'
                        '-0.168053647782867 -4.66595028627023)')
        self.geojson = ('{"type":"LineString","coordinates":['
                        ' [-0.77054223313507,-5.32573853776343],'
                        ' [-0.168053647782867,-4.66595028627023]]}')

    def test_dict_with_geom_is_mandatory(self):
        self.assertRaises(ValidationError, self.f.clean,
                          'LINESTRING(0 0, 1 0)')
        self.assertRaises(ValidationError, self.f.clean,
                          '{"geo": "LINESTRING(0 0, 1 0)"}')

    def test_snaplist_is_mandatory(self):
        self.assertRaises(ValidationError, self.f.clean,
                          '{"geom": "LINESTRING(0 0, 1 0)"}')

    def test_snaplist_must_have_same_number_of_vertices(self):
        self.assertRaises(ValidationError, self.f.clean,
                          '{"geom": "LINESTRING(0 0, 1 0)", "snap": [null]}')

    def test_geom_cannot_be_invalid_wkt(self):
        self.assertRaises(ValidationError, self.f.clean,
                          '{"geom": "LINEPPRING(0 0, 1 0)", '
                          '"snap": [null, null]}')

    def test_geom_can_be_geojson(self):
        geojsonstr = self.geojson.replace('"', '\\"')
        geom = self.f.clean('{"geom": "%s", '
                            ' "snap": [null, null]}' % geojsonstr)
        self.assertTrue(geom.equals_exact(
            LineString((100000, 100000), (200000, 200000),
                       srid=settings.SRID), 0.1))

    def test_geom_is_not_snapped_if_snap_is_null(self):
        value = '{"geom": "%s", "snap": [null, null]}' % self.wktgeom
        self.assertTrue(self.f.clean(value).equals_exact(
            LineString((100000, 100000), (200000, 200000),
                       srid=settings.SRID), 0.1))

    def test_geom_is_snapped_if_path_pk_is_provided(self):
        geom_4326 = GEOSGeometry(self.wktgeom, srid=4326).transform(2154, clone=True)
        last_coords = geom_4326[-1]

        stream = StreamFactory.create()
        coords_stream = [coord for coord in stream.geom.coords]
        coords_stream.append(last_coords)
        stream.geom = LineString(coords_stream, srid=2154)
        stream.save()
        value = '{"geom": "%s", "snap": [null, %s]}' % (self.wktgeom, stream.pk)
        self.assertTrue(self.f.clean(value).equals_exact(
            LineString((100000, 100000), (200000, 200000),
                       srid=settings.SRID), 0.1))


class SnappedGeometryFieldTest(TestCase):
    def setUp(self):
        self.f = SnappedGeometryField()
        self.wktgeom_point = 'POINT(-0.77054223313507 -5.32573853776343)'
        self.wktgeom_linestring = ('LINESTRING(-0.77054223313507 -5.32573853776343,'
                                   '-0.168053647782867 -4.66595028627023)')
        self.wktgeom_polygon = ('POLYGON((-0.77054223313507 -5.32573853776343, -0.57054223313507 -3.32573853776343,'
                                '-0.168053647782867 -4.66595028627023, -0.77054223313507 -5.32573853776343))')
        self.geojson_linestring = ('{"type":"LineString","coordinates":['
                                   ' [-0.77054223313507,-5.32573853776343],'
                                   ' [-0.168053647782867,-4.66595028627023]]}')

    def test_snaplist_must_have_same_number_of_vertices_linestring(self):
        self.assertRaises(ValidationError, self.f.clean,
                          '{"geom": "LINESTRING(0 0, 1 0)", "snap": [null]}')

    def test_snaplist_must_have_same_number_of_vertices_polygon(self):
        self.assertRaises(ValidationError, self.f.clean,
                          '{"geom": "POLYGON((0 0, 1 0, 1 2, 0 0))", "snap": [null, null]}')

    def test_snaplist_must_have_same_number_of_vertices_point(self):
        self.assertRaises(ValidationError, self.f.clean,
                          '{"geom": "POINT(0 0)", "snap": []}')

    def test_linestring_cannot_be_invalid_wkt(self):
        self.assertRaises(ValidationError, self.f.clean,
                          '{"geom": "LINEPPRING(0 0, 1 0)", '
                          '"snap": [null, null]}')

    def test_linestring_is_not_snapped_if_snap_is_null(self):
        value = '{"geom": "%s", "snap": [null, null]}' % self.wktgeom_linestring
        self.assertTrue(self.f.clean(value).equals_exact(
            LineString((100000, 100000), (200000, 200000),
                       srid=settings.SRID), 0.1))

    def test_polygon_is_not_snapped_if_snap_is_null(self):
        value = '{"geom": "%s", "snap": [null, null, null]}' % self.wktgeom_polygon
        self.assertTrue(self.f.clean(value).equals_exact(
            Polygon(((100000, 100000), (145961.3334090858, 411410.4491531737),
                     (200000, 200000), (100000, 100000)),
                    srid=settings.SRID), 0.1))

    def test_point_is_not_snapped_if_snap_is_null(self):
        value = '{"geom": "%s", "snap": [null]}' % self.wktgeom_point
        self.assertTrue(self.f.clean(value).equals_exact(
            Point(100000, 100000, srid=settings.SRID), 0.1))

    def test_linestring_is_snapped_if_path_pk_is_provided(self):
        geom_4326 = GEOSGeometry(self.wktgeom_linestring, srid=4326).transform(2154, clone=True)
        last_coords = geom_4326[-1]

        stream = StreamFactory.create()
        coords_stream = [coord for coord in stream.geom.coords]
        coords_stream.append(last_coords)
        stream.geom = LineString(coords_stream, srid=2154)
        stream.save()

        value = '{"geom": "%s", "snap": [null, %s]}' % (self.wktgeom_linestring, stream.pk)
        self.assertTrue(self.f.clean(value).equals_exact(
            LineString((100000, 100000), (200000, 200000),
                       srid=settings.SRID), 0.1))

    def test_polygon_is_snapped_if_path_pk_is_provided(self):
        """

        Stream's linestring is a random linestring
        0°
                   +
                    \
                     +

        +
        |\
        | \
        |  \
        +--+

          1°
                    +
                     \
                      +
                     /
         +         /
         ||      /
         | |   /
         |  |/
         +--+x

         2°
                    +
                     \
                      +
                     /
         +         /
         ||      /
         | |   /
         |  |/
         +--+ snapped
        """
        # 0°
        geom_4326 = GEOSGeometry(self.wktgeom_polygon, srid=4326).transform(2154, clone=True)
        last_coords = geom_4326.coords[0][-2]

        stream = StreamFactory.create()
        coords_stream = [coord for coord in stream.geom.coords]
        coords_stream.append(last_coords)  # 1°
        stream.geom = LineString(coords_stream, srid=2154)
        stream.save()
        value = '{"geom": "%s", "snap": [null, null, %s]}' % (self.wktgeom_polygon, stream.pk)
        # 2° Snap x on linestring
        self.assertTrue(self.f.clean(value).equals_exact(
            Polygon(((100000, 100000), (145961.3334090858, 411410.4491531737),
                     (200000, 200000), (100000, 100000)),
                    srid=settings.SRID), 0.1))

    def test_point_is_snapped_if_path_pk_is_provided(self):
        geom_4326 = GEOSGeometry(self.wktgeom_point, srid=4326).transform(2154, clone=True)
        last_coords = geom_4326.coords

        stream = StreamFactory.create()
        coords_stream = [coord for coord in stream.geom.coords]
        coords_stream.append(last_coords)  # 1°
        stream.geom = LineString(coords_stream, srid=2154)
        stream.save()
        value = '{"geom": "%s", "snap": [%s]}' % (self.wktgeom_point, stream.pk)
        # 2° Snap x on linestring
        self.assertTrue(self.f.clean(value).equals_exact(
            Point(100000, 100000, srid=settings.SRID), 0.1))
