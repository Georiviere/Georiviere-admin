from django.test import TestCase

from georiviere.description.forms import MorphologyForm, StatusForm
from georiviere.description.models import Morphology, Status
from georiviere.tests.factories import UserAllPermsFactory
from georiviere.river.tests.factories import StreamFactory


class StatusTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = UserAllPermsFactory()
        cls.stream = StreamFactory.create()
        cls.topologies = cls.stream.topologies.all()

        cls.morphology = Morphology.objects.get()
        cls.status = Status.objects.get()

    def test_not_qualified_on_create_topology(self):
        """
        Check if qualified is False on morphology or status creation
        """
        self.assertFalse(self.morphology.topology.qualified)
        self.assertFalse(self.status.topology.qualified)

    def test_morphology_qualified_on_edit(self):
        """
        Check if qualified is True on edit morphology
        """
        morphology_edit_form = MorphologyForm(user=self.user, instance=self.morphology)
        self.assertTrue(morphology_edit_form.fields['qualified'].initial)

    def test_status_qualified_on_edit(self):
        """
        Check if qualified is True on edit status
        """
        status_edit_form = StatusForm(user=self.user, instance=self.status)
        self.assertTrue(status_edit_form.fields['qualified'].initial)
