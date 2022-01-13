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

    def test_simple_usage_outputs_list_of_items(self):
        out = Template(
            '{% load georiviere_tags %}'
            '{% valuelist_source items object %}'
        ).render(Context({
            'object': '',
            'items': ['blah']
        }))
        self.assertHTMLEqual(out.strip(), """<ul><li>blah</li></ul>""")

    def test_obj_list_with_distance_to_source_related_to_stream(self):
        out = Template(
            '{% load georiviere_tags %}'
            '{% valuelist_source items object %}'
        ).render(Context({
            'object': self.stream,
            'items': [self.knowledge]
        }))
        self.assertHTMLEqual(out.strip(), f"""<ul>
        <li class="hoverable" data-modelname="knowledge" data-pk="{self.knowledge.pk}">{self.knowledge.name} (42m)</li>
        </ul>""")

    def test_stream_list_with_distance_to_source_related_to_object(self):
        out = Template(
            '{% load georiviere_tags %}'
            '{% valuelist_source items object %}'
        ).render(Context({
            'object': self.knowledge,
            'items': [self.stream]
        }))
        self.assertHTMLEqual(out.strip(), f"""<ul>
        <li class="hoverable" data-modelname="stream" data-pk="{self.stream.pk}">{self.stream.name} (42m)</li>
        </ul>""")

    def test_can_specify_an_enumeration4(self):
        out = Template(
            '{% load georiviere_tags %}'
            '{% valuelist_source items object enumeration=True %}'
        ).render(Context({
            'object': '',
            'items': range(1, 4)
        }))
        self.assertInHTML('<li><span class="enumeration-value">A.&nbsp;</span>1</li>', out)
        self.assertInHTML('<li><span class="enumeration-value">B.&nbsp;</span>2</li>', out)
        self.assertInHTML('<li><span class="enumeration-value">C.&nbsp;</span>3</li>', out)
