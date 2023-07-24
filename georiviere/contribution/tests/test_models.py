from django.core import mail
from django.test import override_settings, TestCase

from .factories import (ContributionFactory, ContributionPotentialDamageFactory, ContributionQualityFactory,
                        ContributionQuantityFactory, ContributionFaunaFloraFactory,
                        ContributionLandscapeElementsFactory, SeverityTypeTypeFactory, LandingTypeFactory,
                        JamTypeFactory, DiseaseTypeFactory, DeadSpeciesFactory, InvasiveSpeciesFactory,
                        HeritageSpeciesFactory, HeritageObservationFactory, FishSpeciesFactory, NaturePollutionFactory,
                        TypePollutionFactory, ContributionStatusFactory)


@override_settings(MANAGERS=[("Fake", "fake@fake.fake"), ])
class ContributionMetaTest(TestCase):
    """Test for Contribution model"""

    @override_settings(MANAGERS=["fake@fake.fake"])
    def test_contribution_try_send_report_fail(self):
        self.assertEqual(len(mail.outbox), 0)
        contribution = ContributionFactory(email_author='mail.mail@mail')
        self.assertEqual(str(contribution), "mail.mail@mail")
        self.assertEqual(len(mail.outbox), 0)

    def test_contribution_str(self):
        ContributionStatusFactory(label="Informé")
        self.assertEqual(len(mail.outbox), 0)
        contribution = ContributionFactory(email_author='mail.mail@mail')
        self.assertEqual(str(contribution), "mail.mail@mail")
        self.assertEqual(contribution.category, "No category")
        self.assertEqual(len(mail.outbox), 1)

    def test_potentialdamage_str(self):
        self.assertEqual(len(mail.outbox), 0)
        potential_damage = ContributionPotentialDamageFactory(type=2)
        self.assertEqual(str(potential_damage), "Contribution Potential Damage Excessive cutting of riparian forest")
        contribution = potential_damage.contribution
        self.assertEqual(str(contribution),
                         f"{contribution.email_author} "
                         f"Contribution Potential Damage Excessive cutting of riparian forest")
        self.assertEqual(contribution.category, potential_damage)
        self.assertEqual(len(mail.outbox), 1)

    def test_quality_str(self):
        self.assertEqual(len(mail.outbox), 0)
        quality = ContributionQualityFactory(type=2)
        self.assertEqual(str(quality), "Contribution Quality Pollution")
        contribution = quality.contribution
        self.assertEqual(str(contribution),
                         f"{contribution.email_author} "
                         f"Contribution Quality Pollution")
        self.assertEqual(contribution.category, quality)
        self.assertEqual(len(mail.outbox), 1)

    def test_quantity_str(self):
        self.assertEqual(len(mail.outbox), 0)
        quantity = ContributionQuantityFactory(type=2)
        self.assertEqual(str(quantity), "Contribution Quantity In the process of drying out")
        contribution = quantity.contribution
        self.assertEqual(str(contribution),
                         f"{contribution.email_author} "
                         f"Contribution Quantity In the process of drying out")
        self.assertEqual(contribution.category, quantity)
        self.assertEqual(len(mail.outbox), 1)

    def test_fauna_flora_str(self):
        self.assertEqual(len(mail.outbox), 0)
        fauna_flora = ContributionFaunaFloraFactory(type=2)
        self.assertEqual(str(fauna_flora), "Contribution Fauna-Flora Heritage species")
        contribution = fauna_flora.contribution
        self.assertEqual(str(contribution),
                         f"{contribution.email_author} "
                         f"Contribution Fauna-Flora Heritage species")
        self.assertEqual(contribution.category, fauna_flora)
        self.assertEqual(len(mail.outbox), 1)

    def test_landscape_elements_str(self):
        self.assertEqual(len(mail.outbox), 0)
        landscape_elements = ContributionLandscapeElementsFactory(type=2)
        self.assertEqual(str(landscape_elements), "Contribution Landscape Element Fountain")
        contribution = landscape_elements.contribution
        self.assertEqual(str(contribution),
                         f"{contribution.email_author} "
                         f"Contribution Landscape Element Fountain")
        self.assertEqual(contribution.category, landscape_elements)
        self.assertEqual(len(mail.outbox), 1)

    def test_severitytype_str(self):
        severity_type = SeverityTypeTypeFactory(label="Severity type 1")
        self.assertEqual(str(severity_type), "Severity type 1")

    def test_contribution_category_display(self):
        contribution = ContributionFactory(email_author='mail.mail@mail')
        self.assertEqual(str(contribution.category_display),
                         f'<a data-pk="{contribution.pk}" href="/contribution/{contribution.pk}/" title="No category" >No category</a>')
        contribution.published = True
        contribution.save()
        self.assertEqual(contribution.category_display,
                         f'<span class="badge badge-success" title="Published">&#x2606;</span> <a data-pk="{contribution.pk}" href="/contribution/{contribution.pk}/" title="No category" >No category</a>')


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


class ContributionStatusTest(TestCase):
    """Test for Status Contribution model"""

    def test_status_str(self):
        nature_pollution = ContributionStatusFactory(label="Contribution status 1")
        self.assertEqual(str(nature_pollution), "Contribution status 1")
