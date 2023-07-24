from django.test import TestCase

from georiviere.contribution.filters import ContributionFilterSet
from georiviere.contribution.tests.factories import (
    ContributionQualityFactory, ContributionQuantityFactory, ContributionPotentialDamageFactory
)


class ContributionFilterTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.contribution_quality = ContributionQualityFactory.create()
        cls.contribution_quantity = ContributionQuantityFactory.create()
        cls.contribution_potential_damage = ContributionPotentialDamageFactory.create()

    def test_filter_category(self):
        filter = ContributionFilterSet(data={'category_contribution': ['quality', 'potential_damage']})

        self.assertIn(self.contribution_quality.contribution, filter.qs)
        self.assertIn(self.contribution_potential_damage.contribution, filter.qs)
        self.assertEqual(len(filter.qs), 2)

    def test_filter_type(self):
        filter = ContributionFilterSet(data={'type_contribution': ['Dry', 'In the process of drying out']})

        self.assertIn(self.contribution_quantity.contribution, filter.qs)

        self.assertEqual(len(filter.qs), 1)
