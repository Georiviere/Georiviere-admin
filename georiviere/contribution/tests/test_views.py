from georiviere.tests import CommonRiverTest
from . import factories
from georiviere.contribution import models as contribution_models


class ContributionViewTestCase(CommonRiverTest):
    model = contribution_models.Contribution
    modelfactory = factories.ContributionFactory

    def get_expected_json_attrs(self):
        return {
            'id': self.obj.pk,
            'name_author': self.obj.name_author,
            'email_author': self.obj.email_author,
            'description': self.obj.description,
            'first_name_author': self.obj.first_name_author,
            'date_insert': '2020-03-17T00:00:00Z',
            'date_update': '2020-03-17T00:00:00Z',
            'date_observation': '2020-03-17T00:00:00Z',
            'severity': self.obj.severity,
            'geom': self.obj.geom.ewkt,
            'portal': self.obj.portal.pk,
            'published': False
        }

    def test_distance_to_source_is_available(self):
        pass

    def test_crud_status(self):
        if self.model is None:
            return  # Abstract test should not run

        self.login()

        obj = self.modelfactory()

        response = self.client.get(obj.get_list_url())
        self.assertEqual(response.status_code, 200)

        response = self.client.get(obj.get_detail_url().replace(str(obj.pk), '1234567890'))
        self.assertEqual(response.status_code, 404)

        response = self.client.get(obj.get_detail_url())
        self.assertEqual(response.status_code, 200)

        response = self.client.get(obj.get_update_url())
        self.assertEqual(response.status_code, 200)
        self._post_update_form(obj)

        url = obj.get_detail_url()
        obj.delete()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

        # Test to update without login
        self.logout()

        obj = self.modelfactory()

        response = self.client.get(obj.get_update_url())
        self.assertEqual(response.status_code, 302)

    def test_document_export(self):
        pass
