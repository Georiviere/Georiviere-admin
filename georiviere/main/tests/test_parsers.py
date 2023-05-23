from io import StringIO
import requests
from unittest import mock

from django.core.management import call_command
from django.test import TestCase

from geotrek.common.tests import TranslationResetMixin
from georiviere.main.parsers import BiodivParser
from geotrek.sensitivity.models import SportPractice, Species, SensitiveArea


json_test_sport_practice = {
    "count": 2,
    "next": None,
    "previous": None,
    "results": [
        {
            "id": 1,
            "name": {
                "fr": "Terrestre",
                "en": "Land",
                "it": None,
            },
        },
    ],
}

json_test_species = {
    "count": 2,
    "next": "next_page",
    "previous": None,
    "results": [
        {
            "id": 1,
            "url": "https://biodiv-sports.fr/api/v2/sensitivearea/46/?format=json",
            "name": {"fr": "Tétras lyre", "en": "Black grouse", "it": "Fagiano di monte"},
            "description": {"fr": "Blabla", "en": "Blahblah", "it": ""},
            "period": [True, True, True, True, False, False, False, False, False, False, False, True],
            "contact": "",
            "practices": [1],
            "info_url": "",
            "published": True,
            "structure": "LPO",
            "species_id": 7,
            "kml_url": "https://biodiv-sports.fr/api/fr/sensitiveareas/46.kml",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[3.1, 45], [3.2, 45], [3.2, 46], [3.1, 46], [3.1, 45]],
                                [[3.13, 45.3], [3.17, 45.3], [3.17, 45.7], [3.13, 45.7], [3.13, 45.3]]]
            },
            "update_datetime": "2017-11-29T14:53:35.949097Z",
            "create_datetime": "2017-11-29T14:49:01.317155Z",
            "radius": None
        },
    ]
}

json_test_species_page_2 = {
    "count": 2,
    "next": None,
    "previous": None,
    "results": [
        {
            "id": 2,
            "url": "https://biodiv-sports.fr/api/v2/sensitivearea/46/?format=json",
            "name": {"fr": None, "en": None, "it": None},
            "description": {"fr": None, "en": None, "it": None},
            "period": [False, False, False, False, False, False, False, False, False, False, False, False],
            "contact": "",
            "practices": [],
            "info_url": "",
            "published": True,
            "structure": "LPO",
            "species_id": None,
            "kml_url": "https://biodiv-sports.fr/api/fr/sensitiveareas/47.kml",
            "geometry": {
                "type": "MultiPolygon",
                "coordinates": [[[[3.1, 45], [3.2, 45], [3.2, 46], [3.1, 46], [3.1, 45]],
                                 [[3.13, 45.3], [3.17, 45.3], [3.17, 45.7], [3.13, 45.7], [3.13, 45.3]],
                                 [[3.145, 45.45], [3.155, 45.45], [3.155, 45.55], [3.145, 45.55], [3.145, 45.45]],
                                 [[3.14, 45.4], [3.16, 45.4], [3.16, 45.6], [3.14, 45.6], [3.14, 45.4]],
                                 [[3.11, 45.45], [3.12, 45.45], [3.12, 45.55], [3.11, 45.55], [3.11, 45.45]]],
                                [[[3.1, 45], [3.2, 45], [3.2, 46], [3.1, 46], [3.1, 45]]]
                                ]
            },
            "update_datetime": "2017-11-29T14:53:35.949097Z",
            "create_datetime": "2017-11-29T14:49:01.317155Z",
            "radius": None
        }
    ]
}


class BiodivWithoutPracticeParser(BiodivParser):
    size = 1


class BiodivWithPracticeParser(BiodivParser):
    practices = "1"
    size = 1


class BiodivParserTests(TranslationResetMixin, TestCase):
    @mock.patch('requests.get')
    def test_create(self, mocked):
        self.page = 1

        def side_effect(url, allow_redirects, params=None):
            response = requests.Response()
            response.status_code = 200

            if 'sportpractice' in url:
                response.json = lambda: json_test_sport_practice
            else:
                if self.page == 1:
                    response.json = lambda: json_test_species
                    self.page += 1
                else:
                    response.json = lambda: json_test_species_page_2
            return response
        mocked.side_effect = side_effect
        output = StringIO()
        call_command('import', 'georiviere.main.tests.test_parsers.BiodivWithPracticeParser', verbosity=2,
                     stdout=output)
        practice = SportPractice.objects.first()
        species = Species.objects.first()
        area_1 = SensitiveArea.objects.first()
        self.assertEqual(practice.name, "Land")
        self.assertEqual(practice.name_fr, "Terrestre")
        self.assertEqual(species.name, "Black grouse")
        self.assertEqual(species.name_fr, "Tétras lyre")
        self.assertTrue(species.period01)
        self.assertFalse(species.period06)
        self.assertEqual(species.eid, '7')
        self.assertQuerysetEqual(species.practices.all(), ['<SportPractice: Land>'], transform=repr)
        self.assertEqual(area_1.species, species)
        self.assertEqual(area_1.description, "Blahblah")
        self.assertEqual(area_1.description_fr, "Blabla")
        self.assertEqual(area_1.eid, '1')
        area_2 = SensitiveArea.objects.last()
        self.assertQuerysetEqual(species.practices.all(), ['<SportPractice: Land>'], transform=repr)
        self.assertEqual(area_2.species, species)
        self.assertEqual(area_2.description, "Blahblah2")
        self.assertEqual(area_2.description_fr, "Blabla2")
        self.assertEqual(area_2.eid, '2')
        self.assertEqual(area_2.geom.geom_type, 'MultiPolygon')
