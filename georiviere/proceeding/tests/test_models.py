from django.test import TestCase

from georiviere.proceeding.tests import factories


class ProceedingTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.proceeding = factories.ProceedingFactory.create()
        cls.event_type = factories.EventTypeFactory.create()
        cls.event = factories.EventFactory.create(proceeding=cls.proceeding, event_type=cls.event_type)

    def test_str_proceeding(self):
        self.assertEqual(str(self.proceeding), f"{self.proceeding.name} :  2002-02-20")

    def test_str_event(self):
        self.assertEqual(str(self.event), f"{self.event_type.name} :  2002-02-20")

    def test_str_event_type(self):
        self.assertEqual(str(self.event_type), f"{self.event_type.name}")
