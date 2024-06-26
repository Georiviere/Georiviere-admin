from django.test import TestCase
from django.urls import reverse

from georiviere.portal.tests.factories import PortalFactory
from georiviere.river.tests.factories import StreamFactory


class StreamViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.portal = PortalFactory.create()
        cls.stream = StreamFactory.create()
        cls.stream.portals.add(cls.portal)

    def test_stream_detail_geojson_structure(self):
        url = reverse(
            "api_portal:streams-detail",
            kwargs={
                "portal_pk": self.portal.pk,
                "pk": self.stream.pk,
                "lang": "fr",
                "format": "geojson",
            },
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertSetEqual(
            set(response.json().keys()), {"geometry", "properties", "type"}
        )

    def test_stream_detail_json_structure(self):
        url = reverse(
            "api_portal:streams-detail",
            kwargs={
                "portal_pk": self.portal.pk,
                "pk": self.stream.pk,
                "lang": "fr",
                "format": "json",
            },
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(
            sorted(list(response.json().keys())),
            sorted([
                "attachments",
                "length",
                "flow",
                "descent",
                "name",
                "id",
                "description",
                "geometryCenter",
                "geojsonUrl",
                "jsonUrl",
            ]),
        )

    def test_stream_list_geojson_structure(self):
        url = reverse(
            "api_portal:streams-list",
            kwargs={"portal_pk": self.portal.pk, "lang": "fr", "format": "geojson"},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertSetEqual(set(response.json().keys()), {"type", "features"})

    def test_stream_list_json_structure(self):
        url = reverse(
            "api_portal:streams-list",
            kwargs={"portal_pk": self.portal.pk, "lang": "fr", "format": "json"},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertListEqual(
            sorted(list(response.json()[0].keys())),
            sorted([
                "attachments",
                "length",
                "flow",
                "descent",
                "name",
                "id",
                "description",
                "geometryCenter",
                "geojsonUrl",
                "jsonUrl",
            ]),
        )

    def test_stream_ranslation_according_url(self):
        for lang in ["en", "fr"]:
            url = reverse(
                "api_portal:streams-detail",
                kwargs={
                    "portal_pk": self.portal.pk,
                    "pk": self.stream.pk,
                    "lang": lang,
                    "format": "json",
                },
            )
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(
                data["flow"], "To be defined" if lang == "en" else "À définir"
            )
