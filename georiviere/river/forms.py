from django import forms
from django.contrib.gis.geos import Point

from geotrek.common.forms import CommonForm

from georiviere.river.fields import SnappedLineStringField
from georiviere.river.models import Stream, Topology


class StreamForm(CommonForm):
    geom = SnappedLineStringField()

    geomfields = ['geom']

    class Meta:
        fields = "__all__"
        model = Stream

    def save(self, commit=True):
        """Set source_location on creation with stream geom first point, if it is not set in form"""
        if not self.update and not self.cleaned_data['source_location']:
            self.instance.source_location = Point(self.instance.geom[0])
        return super().save(commit)


class TopologyRiverForm(CommonForm):
    class Media:
        js = ('river/js/remove_delete_button.js', )


class CutTopologyForm(forms.Form):
    topology = forms.ModelChoiceField(queryset=Topology.objects.all(), widget=forms.widgets.HiddenInput())
    lat = forms.FloatField(widget=forms.HiddenInput())
    lng = forms.FloatField(widget=forms.HiddenInput())
