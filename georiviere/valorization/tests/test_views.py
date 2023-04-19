from collections import OrderedDict
from tempfile import TemporaryDirectory

from django.test import override_settings
from django.utils.translation import gettext_lazy as _
from geotrek.authent.tests.factories import StructureFactory

from georiviere.tests import CommonRiverTest
from .factories import POIKnowledgeFactory, POIKnowledgeTypeFactory, POIActionFactory, POIActionTypeFactory

from ..models import POIKnowledge, POIAction


@override_settings(MEDIA_ROOT=TemporaryDirectory().name)
class POIKnowledgeViewTestCase(CommonRiverTest):
    model = POIKnowledge
    modelfactory = POIKnowledgeFactory

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
        poiknowledgetype = POIKnowledgeTypeFactory.create()
        temp_data = self.modelfactory.build(structure=structure, type=poiknowledgetype)
        return {
            'structure': structure.pk,
            'geom': temp_data.geom.ewkt,
            'name': temp_data.name,
            'description': temp_data.description,
            'type': poiknowledgetype.pk,
            'portals': [],
        }


@override_settings(MEDIA_ROOT=TemporaryDirectory().name)
class POIActionViewTestCase(CommonRiverTest):
    model = POIAction
    modelfactory = POIActionFactory

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
        poiactiontype = POIActionTypeFactory.create()
        temp_data = self.modelfactory.build(structure=structure, type=poiactiontype)
        return {
            'structure': structure.pk,
            'geom': temp_data.geom.ewkt,
            'name': temp_data.name,
            'description': temp_data.description,
            'type': poiactiontype.pk,
            'portals': [],
        }
