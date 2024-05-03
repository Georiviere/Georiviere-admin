from django.conf import settings
from django.contrib.gis.forms.fields import PointField
from django import forms

from crispy_forms.layout import Div, Field

from geotrek.common.forms import CommonForm

from georiviere.valorization.models import POI, POICategory


class POIForm(CommonForm):
    geom = PointField(srid=settings.SRID)
    category = forms.ModelChoiceField(label="Category", queryset=POICategory.objects)

    geomfields = ['geom']

    fieldslayout = [
        Div(
            'name',
            'description',
            'external_uri',
            Field('portals', css_class="chzn-select"),
            'category',
            'type',
        )
    ]

    class Meta:
        model = POI
        fields = ['name', 'description', 'external_uri', 'type', 'category', 'portals', 'geom']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['category'].initial = self.instance.type.category.pk
