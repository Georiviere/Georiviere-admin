from django.test import TestCase

from . import factories


class KnowledgeTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.knowledge = factories.KnowledgeFactory(
            name="Avancée érosion berges",
        )

    def test_str(self):
        self.assertEqual(str(self.knowledge), "Avancée érosion berges")


class FollowUpTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.follow_up = factories.FollowUpFactory(
            name="Avancée érosion berges",
        )

    def test_str(self):
        self.assertEqual(str(self.follow_up), "Avancée érosion berges")
