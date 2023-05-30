from django.test import TestCase

from .factories import (ContributionFactory, ContributionPotentialDamageFactory, ContributionQualityFactory,
                        ContributionQuantityFactory, ContributionFaunaFloraFactory,
                        ContributionLandscapeElementsFactory, SeverityTypeTypeFactory, LandingTypeFactory,
                        JamTypeFactory, DiseaseTypeFactory, DeadSpeciesFactory, InvasiveSpeciesFactory,
                        HeritageSpeciesFactory, HeritageObservationFactory, FishSpeciesFactory, NaturePollutionFactory,
                        TypePollutionFactory)


class ContributionCategoriesTest(TestCase):
    """Test for Category Contribution model"""

    def test_contribution_str(self):
        contribution = ContributionFactory(email_author='mail.mail@mail')
        self.assertEqual(str(contribution), "mail.mail@mail")
        self.assertEqual(contribution.category, "No category")

    def test_potentialdamage_str(self):
        potential_damage = ContributionPotentialDamageFactory(type=2)
        self.assertEqual(str(potential_damage), "Contribution Potential Damage Excessive cutting of riparian forest")
        contribution = potential_damage.contribution
        self.assertEqual(str(contribution),
                         f"{contribution.email_author} "
                         f"Contribution Potential Damage Excessive cutting of riparian forest")
        self.assertEqual(contribution.category, potential_damage)

    def test_quality_str(self):
        quality = ContributionQualityFactory(type=2)
        self.assertEqual(str(quality), "Contribution Quality Pollution")
        contribution = quality.contribution
        self.assertEqual(str(contribution),
                         f"{contribution.email_author} "
                         f"Contribution Quality Pollution")
        self.assertEqual(contribution.category, quality)

    def test_quantity_str(self):
        quantity = ContributionQuantityFactory(type=2)
        self.assertEqual(str(quantity), "Contribution Quantity In the process of drying out")
        contribution = quantity.contribution
        self.assertEqual(str(contribution),
                         f"{contribution.email_author} "
                         f"Contribution Quantity In the process of drying out")
        self.assertEqual(contribution.category, quantity)

    def test_fauna_flora_str(self):
        fauna_flora = ContributionFaunaFloraFactory(type=2)
        self.assertEqual(str(fauna_flora), "Contribution Fauna-Flora Heritage species")
        contribution = fauna_flora.contribution
        self.assertEqual(str(contribution),
                         f"{contribution.email_author} "
                         f"Contribution Fauna-Flora Heritage species")
        self.assertEqual(contribution.category, fauna_flora)

    def test_landscape_elements_str(self):
        landscape_elements = ContributionLandscapeElementsFactory(type=2)
        self.assertEqual(str(landscape_elements), "Contribution Landscape Element Fountain")
        contribution = landscape_elements.contribution
        self.assertEqual(str(contribution),
                         f"{contribution.email_author} "
                         f"Contribution Landscape Element Fountain")
        self.assertEqual(contribution.category, landscape_elements)

    def test_severitytype_str(self):
        severity_type = SeverityTypeTypeFactory(label="Severity type 1")
        self.assertEqual(str(severity_type), "Severity type 1")


class ContributionPotentialDamageTest(TestCase):
    """Test for Category potential damage model"""

    def test_landingtype_str(self):
        landing_type = LandingTypeFactory(label="Landing type 1")
        self.assertEqual(str(landing_type), "Landing type 1")

    def test_jamtype_str(self):
        jam_type = JamTypeFactory(label="Jam type 1")
        self.assertEqual(str(jam_type), "Jam type 1")

    def test_diseasetype_str(self):
        disease_type = DiseaseTypeFactory(label="Disease type 1")
        self.assertEqual(str(disease_type), "Disease type 1")

    def test_deadspecies_str(self):
        dead_species = DeadSpeciesFactory(label='Dead species 1')
        self.assertEqual(str(dead_species), "Dead species 1")


class ContributionFaunaFloraTest(TestCase):
    """Test for Category potential damage model"""

    def test_invasivespecies_str(self):
        invasive_species = InvasiveSpeciesFactory(label="Invasive species 1")
        self.assertEqual(str(invasive_species), "Invasive species 1")

    def test_heritagespecies_str(self):
        heritage_species = HeritageSpeciesFactory(label="Heritage species 1")
        self.assertEqual(str(heritage_species), "Heritage species 1")

    def test_heritageobservations_str(self):
        heritage_observation = HeritageObservationFactory(label="Heritage observation 1")
        self.assertEqual(str(heritage_observation), "Heritage observation 1")

    def test_fishspecies_str(self):
        fish_species = FishSpeciesFactory(label="Fish species 1")
        self.assertEqual(str(fish_species), "Fish species 1")


class ContributionNaturePollutionTest(TestCase):
    """Test for Category potential damage model"""

    def test_naturepollution_str(self):
        nature_pollution = NaturePollutionFactory(label="Nature pollution 1")
        self.assertEqual(str(nature_pollution), "Nature pollution 1")

    def test_typepollution_str(self):
        type_pollution = TypePollutionFactory(label="Type pollution 1")
        self.assertEqual(str(type_pollution), "Type pollution 1")
