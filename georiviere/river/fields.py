import logging
import json

from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.gis.forms.fields import GeometryField, LineStringField
from django.contrib.gis.geos import fromstr, Point, LineString

from .models import Stream
from .widgets import SnappedGeometryWidget


logger = logging.getLogger(__name__)


class SnappedFieldMixin(object):
    """
    It's a LineString field, with additional information about snapped vertices.
    """
    widget = SnappedGeometryWidget

    default_error_messages = {
        'invalid_snap_line': _('Geometry invalid snapping.'),
    }

    def clean(self, value):
        """
        A serialized dict is received, with ``geom`` and ``snaplist``.
        We use ``snaplist`` to snap geometry vertices.
        """
        if value in validators.EMPTY_VALUES:
            return super().clean(value)
        try:
            value = json.loads(value)
            geom = value.get('geom')
            if geom is None:
                raise ValueError("No geom found in JSON")

            if geom in validators.EMPTY_VALUES:
                return super().clean(value)

            # Geometry is like usual
            geom = fromstr(geom)
            if geom is None:
                raise ValueError("Invalid geometry in JSON")
            geom.srid = settings.API_SRID
            geom.transform(settings.SRID)

            # We have the list of snapped paths, we use them to modify the
            # geometry vertices
            snaplist = value.get('snap', [])
            if geom.num_coords != len(snaplist):
                raise ValueError("Snap list length != %s (%s)" % (geom.num_coords, snaplist))
            paths = [Stream.objects.get(pk=pk) if pk is not None else None
                     for pk in snaplist]
            coords = list(geom.coords)
            for i, (vertex, path) in enumerate(zip(coords, paths)):
                if path:
                    # Snap vertex on path
                    snap = path.snap(Point(*vertex, srid=geom.srid))
                    coords[i] = snap.coords
            return LineString(*coords, srid=settings.SRID)
        except (TypeError, Stream.DoesNotExist, ValueError) as e:
            logger.warning("User input error: %s" % e)
            raise ValidationError(self.error_messages['invalid_snap_line'])


class SnappedGeometryField(SnappedFieldMixin, GeometryField):
    pass


class SnappedLineStringField(SnappedFieldMixin, LineStringField):
    default_error_messages = {
        'invalid_snap_line': _('Linestring invalid snapping.'),
    }
