from django.test import TestCase

from georiviere.river.models import Stream
from georiviere.river.tests.factories import StreamFactory


class RiverManagerTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        StreamFactory.create_batch(5)

    def test_truncate(self):
        self.assertEqual(Stream.objects.count(), 5)
        Stream.objects.truncate()
        self.assertEqual(Stream.objects.count(), 0)
