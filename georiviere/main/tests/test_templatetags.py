from unittest import mock
from django.template import Template, Context
from django.test import TestCase
from django.utils import translation

from georiviere.river.tests.factories import StreamFactory
from georiviere.knowledge.tests.factories import KnowledgeFactory


class ValueListTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        translation.deactivate()
        cls.stream = StreamFactory(name='A river')
        cls.knowledge = KnowledgeFactory(name='A bridge')

    def test_empty_list_should_show_none(self):
        out = Template(
            '{% load georiviere_tags %}'
            '{% valuelist_source items object %}'
        ).render(Context({
            'object': '',
            'items': []
        }))
        self.assertHTMLEqual(out.strip(), '<span class="none">None</span>')

    @mock.patch('georiviere.river.models.Stream.distance_to_source')
    def test_obj_list_with_distance_to_source_related_to_stream(self, mock_distance_to_source):
        mock_distance_to_source.return_value = 42.63
        out = Template(
            '{% load georiviere_tags %}'
            '{% valuelist_source items stream %}'
        ).render(Context({
            'stream': self.stream,
            'items': [self.knowledge]
        }))
        self.assertHTMLEqual(out.strip(), f"""<ul>
        <li class="hoverable" data-modelname="knowledge" data-pk="{self.knowledge.pk}">{self.knowledge.name}
        (42.6 m)</li>
        </ul>""")

    @mock.patch('georiviere.river.models.Stream.distance_to_source')
    def test_obj_list_with_distance_to_source_related_to_stream_with_field(self, mock_distance_to_source):
        mock_distance_to_source.return_value = 42.63
        out = Template(
            '{% load georiviere_tags %}'
            '{% valuelist_source items stream "name" %}'
        ).render(Context({
            'stream': self.stream,
            'items': [self.knowledge]
        }))
        self.assertHTMLEqual(out.strip(), f"""<ul>
        <li class="hoverable" data-modelname="knowledge" data-pk="{self.knowledge.pk}">
        <a data-pk="{self.knowledge.pk}" href="/knowledge/{self.knowledge.pk}/" title="{self.knowledge.name}">
        {self.knowledge.name}</a>
        (42.6 m)</li>
        </ul>""")

    @mock.patch('georiviere.river.models.Stream.distance_to_source')
    def test_stream_list_with_distance_to_source_related_to_object(self, mock_distance_to_source):
        mock_distance_to_source.return_value = 42.63
        out = Template(
            '{% load georiviere_tags %}'
            '{% valuelist_streams streams object %}'
        ).render(Context({
            'object': self.knowledge,
            'streams': [self.stream]
        }))
        self.assertHTMLEqual(out.strip(), f"""<ul>
        <li class="hoverable" data-modelname="stream" data-pk="{self.stream.pk}">
        <a data-pk="{self.stream.pk}" href="/stream/{self.stream.pk}/" title="{self.stream.name}">
        {self.stream.name}</a>
        (42.6 m)</li>
        </ul>""")
