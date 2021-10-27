from collections import OrderedDict

from geotrek.authent.factories import StructureFactory
from georiviere.tests import CommonRiverTest

from studies.factories import StudyFactory, StudyTypeFactory
from studies.models import Study


class StudyViewTestCase(CommonRiverTest):
    model = Study
    modelfactory = StudyFactory

    def get_expected_json_attrs(self):
        return {
            'id': self.obj.pk,
            'date_insert': '2020-03-17T00:00:00Z',
            'date_update': '2020-03-17T00:00:00Z',
            'description': self.obj.description,
            'geom': self.obj.geom.ewkt,
            'structure': self.obj.structure.pk,
            'study_types': [],
            'title': self.obj.title,
            'study_authors': self.obj.study_authors,
            'year': self.obj.year,
        }

    def get_bad_data(self):
        return OrderedDict([
            ('title', ''),
        ]), 'This field is required.'

    def get_good_data(self):
        structure = StructureFactory.create()
        study_type1 = StudyTypeFactory.create()
        study_type2 = StudyTypeFactory.create()
        temp_data = self.modelfactory.build(
            structure=structure,
        )
        return {
            'structure': structure.pk,
            'geom': temp_data.geom.ewkt,
            'study_types': [study_type1.pk, study_type2.pk],
            'title': 'test',
            'year': 2012,
        }
