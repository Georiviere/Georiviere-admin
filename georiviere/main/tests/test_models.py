from django.test import TestCase
from geotrek.authent.tests.factories import StructureFactory, UserFactory

from georiviere.valorization.tests.factories import POIFactory
from .factories import AttachmentFactory, DataSourceFactory


class DataSourceTest(TestCase):
    """Test for Data source model"""

    def test_str(self):
        data_source = DataSourceFactory(name="Jouvence")
        self.assertEqual(str(data_source), "Jouvence")

        data_source.structure = StructureFactory(name="Ma petite entreprise")
        data_source.save()
        self.assertEqual(str(data_source), "Jouvence (Ma petite entreprise)")


class AttachmentTest(TestCase):
    """Test for Attachment model"""

    def test_str(self):
        poi = POIFactory.create()
        creator = UserFactory.create()
        attachment = AttachmentFactory(creator=creator, content_object=poi)
        self.assertIn(f'{creator.username}', str(attachment))

        attachment_without_creator = AttachmentFactory(content_object=poi, creator=None)
        self.assertNotIn('attached', str(attachment_without_creator))
