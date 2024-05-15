from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from georiviere.contribution.tests.factories import CustomContributionTypeFactory
from georiviere.observations.tests.factories import StationFactory
from georiviere.portal.tests.factories import PortalFactory


class StationViewSetTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.portal = PortalFactory()
        cls.station_linked_to_type = StationFactory()
        cls.custom_contribution_type = CustomContributionTypeFactory()
        cls.custom_contribution_type.stations.add(cls.station_linked_to_type)
        cls.station_not_linked = StationFactory()

    def test_only_station_linked_to_type_are_returned(self):
        response = self.client.get(
            reverse(
                "api_portal:stations-list",
                kwargs={"portal_pk": self.portal.pk, "lang": "fr"},
            )
        )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.station_linked_to_type.pk)

    def test_detail_station_linked_to_type(self):
        response = self.client.get(
            reverse(
                "api_portal:stations-detail",
                kwargs={
                    "portal_pk": 1,
                    "lang": "fr",
                    "pk": self.station_linked_to_type.pk,
                },
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_list_geojson(self):
        response = self.client.get(
            reverse(
                "api_portal:stations-list",
                kwargs={"portal_pk": self.portal.pk, "lang": "fr", "format": "geojson"},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("features", response.json())

    def test_detail_geojson(self):
        response = self.client.get(
            reverse(
                "api_portal:stations-detail",
                kwargs={
                    "portal_pk": 1,
                    "lang": "fr",
                    "format": "geojson",
                    "pk": self.station_linked_to_type.pk,
                },
            )
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("properties", data)
        self.assertIn("geometry", data)
