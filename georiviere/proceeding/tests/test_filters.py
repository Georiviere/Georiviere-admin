from django.test import TestCase
from geotrek.authent.tests.factories import StructureFactory

from georiviere.proceeding.filters import ProceedingFilterSet
from .factories import ProceedingFactory, EventTypeFactory, EventFactory


class ProceedingFilterTestCase(TestCase):
    """Test filter on parameter tracked"""

    def setUp(self):
        self.structure = StructureFactory.create()
        self.proceeding1 = ProceedingFactory.create(
            structure=self.structure,
        )
        self.proceeding2 = ProceedingFactory.create(
            structure=self.structure,
        )
        self.proceeding3 = ProceedingFactory.create(
            structure=self.structure,
        )
        self.proceeding4 = ProceedingFactory.create(
            structure=self.structure,
        )
        self.event_type1 = EventTypeFactory.create()
        self.event1 = EventFactory.create(
            proceeding=self.proceeding1,
            event_type=self.event_type1
        )
        self.event2 = EventFactory.create(
            proceeding=self.proceeding2,
            event_type=self.event_type1
        )

    def test_filter_proceeding_on_event_type(self):
        """Test filter on parameter tracked"""
        filterset = ProceedingFilterSet({'event_type': [self.event_type1]})
        self.assertEqual(filterset.qs.count(), 2)
