from django.test import TestCase

from georiviere.description.models import Morphology, Status
from georiviere.river.tests.factories import StreamFactory


class SignalRiverTest(TestCase):
    def test_create_stream_generate_topologies(self):
        stream = StreamFactory.create()
        self.assertEqual(str(stream), stream.name)

        topologies = stream.topologies.all()

        morphology = Morphology.objects.get()
        status = Status.objects.get()

        self.assertIn(morphology.topology, topologies)
        self.assertIn(status.topology, topologies)
        self.assertTrue(morphology.geom.equals_exact(stream.geom, 0.001))
        self.assertTrue(status.geom.equals_exact(stream.geom, 0.001))

    def test_update_stream_move_topologies(self):
        stream = StreamFactory.create()
        stream_2 = StreamFactory.create()
        stream.geom = stream_2.geom
        stream.save()

        self.assertEqual(str(stream), stream.name)

        stream_1_morpho_geom = stream.morphologies.first().geom.ewkt
        stream_2_morpho_geom = stream_2.morphologies.first().geom.ewkt

        status = Status.objects.values_list("geom", flat=True)

        self.assertEqual(
            stream_1_morpho_geom,
            stream_2_morpho_geom,
            f"{stream_1_morpho_geom} - {stream_2_morpho_geom}",
        )
        self.assertEqual(status[0], status[1])
