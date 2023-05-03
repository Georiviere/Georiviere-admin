from collections import OrderedDict
from tempfile import TemporaryDirectory

from django.test import override_settings
from django.utils.translation import gettext_lazy as _
from geotrek.authent.tests.factories import StructureFactory

from georiviere.tests import CommonRiverTest
from .factories import POIFactory, POITypeFactory, POICategoryFactory

from ..models import POI


@override_settings(MEDIA_ROOT=TemporaryDirectory().name)
class POIViewTestCase(CommonRiverTest):
    model = POI
    modelfactory = POIFactory

    def get_bad_data(self):
        return OrderedDict([('name', ''),
                            ('geom', 'POINT(0 0)')]), _('This field is required.')

    def get_expected_json_attrs(self):
        return {
            'id': self.obj.pk,
            'structure': self.obj.structure.pk,
            'date_update': '2020-03-17T00:00:00Z',
            'date_insert': '2020-03-17T00:00:00Z',
            'description': self.obj.description,
            'geom': self.obj.geom.ewkt,
            'type': self.obj.type.pk,
            'name': self.obj.name,
            'portals': []
        }

    def get_good_data(self):
        structure = StructureFactory.create()
        poicategory = POICategoryFactory.create()
        poitype = POITypeFactory.create(category=poicategory)
        temp_data = self.modelfactory.build(structure=structure, type=poitype)
        return {
            'structure': structure.pk,
            'geom': temp_data.geom.ewkt,
            'name': temp_data.name,
            'description': temp_data.description,
            'category': poicategory.pk,
            'type': poitype.pk,
            'portals': [],
        }
