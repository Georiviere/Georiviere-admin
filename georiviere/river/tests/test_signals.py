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
        stream.refresh_from_db()

        self.assertEqual(str(stream), stream.name)

        stream_1_morpho_geom = stream.morphologies[0].geom
        stream_2_morpho_geom = stream_2.morphologies[0].geom

        self.assertEqual(len(stream.morphologies), 1)
        self.assertEqual(len(stream_2.morphologies), 1)
        status = Status.objects.values_list("geom", flat=True)
        self.assertEqual(stream_1_morpho_geom.length, stream_1_morpho_geom.length)
        self.assertEqual(
            stream_1_morpho_geom.ewkt,
            stream_2_morpho_geom.ewkt,
            f"{stream_1_morpho_geom.ewkt} - {stream_2_morpho_geom.ewkt}",
        )
        self.assertEqual(status[0], status[1])
