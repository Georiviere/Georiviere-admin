from django.contrib.contenttypes.models import ContentType

from georiviere.tests import CommonRiverTest
from . import factories
from georiviere.contribution import models as contribution_models
from georiviere.knowledge.models import Knowledge
from georiviere.knowledge.tests.factories import KnowledgeFactory
from georiviere.portal.tests.factories import PortalFactory


class ContributionViewTestCase(CommonRiverTest):
    model = contribution_models.Contribution
    modelfactory = factories.ContributionFactory

    def get_expected_json_attrs(self):
        return {
            'id': self.obj.pk,
            'assigned_user': self.obj.assigned_user,
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
            'published': False,
            'status_contribution': self.obj.status_contribution,
            'validated': False,
            'publication_date': self.obj.publication_date,
            'linked_object_type': None,
            'linked_object_id': None,
        }

    def get_good_data(self):
        portal = PortalFactory.create()
        severity = factories.SeverityTypeTypeFactory()
        temp_data = self.modelfactory.build(portal=portal)
        knowledge = KnowledgeFactory.create()
        return {
            'email_author': temp_data.email_author,
            'portal': portal.pk,
            'geom': temp_data.geom.ewkt,
            'severity': severity.pk,
            'description': 'New_description',
            'linked_object_id': knowledge.pk,
            'linked_object_type': ContentType.objects.get_for_model(Knowledge)
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

        obj.linked_object = KnowledgeFactory.create()
        obj.save()

        response = self.client.get(obj.get_detail_url())
        self.assertEqual(response.status_code, 200)

        response = self.client.get(obj.get_update_url())
        self.assertEqual(response.status_code, 200)
        self._post_update_form(obj)

        response = self.client.get(obj.get_update_url())
        self.assertEqual(response.status_code, 200)
        good_data_without_linked_object = self.get_good_data()
        good_data_without_linked_object['linked_object'] = ""
        response = self.client.post(obj.get_update_url(), good_data_without_linked_object)
        if response.status_code != 302:
            form = self.get_form(response)
            self.assertEqual(form.errors, [])  # this will show form errors

        self.assertEqual(response.status_code, 302)  # success, redirects to detail view

        url = obj.get_detail_url()
        obj.delete()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

        # Test to update without login
        self.logout()

        obj = self.modelfactory()

        response = self.client.get(obj.get_update_url())
        self.assertEqual(response.status_code, 302)

        # Test to delete object
        self.login()

        response = self.client.get(obj.get_update_url())
        self.assertEqual(response.status_code, 200)

    def test_document_export(self):
        pass
