from django.test import TestCase

from georiviere.description.tests.factories import MorphologyFactory, StatusFactory
from georiviere.river.tests.factories import TopologyFactory


class TopologyTest(TestCase):

    def test_str(self):
        morphology = MorphologyFactory.create()
        status = StatusFactory.create()
        lonely_topology = TopologyFactory()
        self.assertEqual(str(status.topology), "Status {}".format(status.pk))
        self.assertEqual(str(morphology.topology), "Morphology {}".format(morphology.pk))
        self.assertEqual(str(lonely_topology), "Topology {}".format(lonely_topology.pk))
