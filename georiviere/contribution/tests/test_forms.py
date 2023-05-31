from django.test import TestCase

from georiviere.tests.factories import UserAllPermsFactory
from . import factories
from ..forms import ContributionForm


class ContributionFormTestCase(TestCase):
    """Test form contribution"""

    @classmethod
    def setUpTestData(cls):

        cls.user = UserAllPermsFactory()
        cls.quantity = factories.ContributionQuantityFactory()

    def test_contribution(self):
        self.client.force_login(self.user)
        contribution_form = ContributionForm(user=self.user, instance=self.quantity.contribution,
                                             data={"geom": self.quantity.contribution.geom,
                                                   "email_author": self.quantity.contribution.email_author},
                                             can_delete=False)
        self.assertEqual(True, contribution_form.is_valid())
