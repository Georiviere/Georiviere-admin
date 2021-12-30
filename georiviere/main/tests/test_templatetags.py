from django.template import Template, Context
from django.test import TestCase
from django.utils import translation

from georiviere.river.models import Stream
from georiviere.river.tests.factories import StreamFactory


class ValueListTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        translation.deactivate()
        cls.obj = StreamFactory(name='blah')

    def test_empty_list_should_show_none(self):
        out = Template(
            '{% load georiviere_tags %}'
            '{% valuelist_source items %}'
        ).render(Context({
            'items': []
        }))
        self.assertHTMLEqual(out.strip(), '<span class="none">None</span>')

    def test_simple_usage_outputs_list_of_items(self):
        out = Template(
            '{% load georiviere_tags %}'
            '{% valuelist_source items %}'
        ).render(Context({
            'items': ['blah']
        }))
        self.assertHTMLEqual(out.strip(), """<ul><li>blah</li></ul>""")

    def test_can_specify_field_to_be_used(self):
        out = Template(
            '{% load georiviere_tags %}'
            '{% valuelist_source items field="name" %}'
        ).render(Context({
            'items': [self.obj]
        }))
        self.assertHTMLEqual(out.strip(), """<ul>
        <li class="hoverable" data-modelname="stream" data-pk="1">
        <a data-pk="1" href="/stream/1/" title="blah">blah</a></li>
        </ul>""")

    def test_obj_with_distance_to_source(self):
        out = Template(
            '{% load georiviere_tags %}'
            '{% valuelist_source items %}'
        ).render(Context({
            'items': [self.obj]
        }))
        self.assertHTMLEqual(out.strip(), """<ul>
        <li class="hoverable" data-modelname="stream" data-pk="1">blah (42m)</li>
        </ul>""")

    def test_can_specify_an_enumeration4(self):
        out = Template(
            '{% load georiviere_tags %}'
            '{% valuelist_source items enumeration=True %}'
        ).render(Context({
            'items': range(1, 4)
        }))
        self.assertInHTML('<li><span class="enumeration-value">A.&nbsp;</span>1</li>', out)
        self.assertInHTML('<li><span class="enumeration-value">B.&nbsp;</span>2</li>', out)
        self.assertInHTML('<li><span class="enumeration-value">C.&nbsp;</span>3</li>', out)
