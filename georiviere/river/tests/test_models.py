from django.test import TestCase

from georiviere.description.tests import factories as description_factories


class TopologyTest(TestCase):

    def test_str(self):
        morphology = description_factories.MorphologyFactory.create()
        status = description_factories.StatusFactory.create()
        self.assertEqual(str(status.topology), "Status {}".format(status.pk))
        self.assertEqual(str(morphology.topology), "Morpho {}".format(morphology.pk))
