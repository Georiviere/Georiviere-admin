from django.test import TestCase

from studies import factories


class StudyTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.study = factories.StudyFactory(
            title="Étude algues lac des Rousses",
        )

    def test_str(self):
        self.assertEqual(str(self.study), "Étude algues lac des Rousses")
