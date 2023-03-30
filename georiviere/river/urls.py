from django.urls import path, register_converter, converters
from geotrek.altimetry.urls import AltimetryEntityOptions

from georiviere.river.views import (CutTopologyView, DistanceToSourceView, StreamDocumentReport,
                                    StreamStudyViewSet, StreamUsageViewSet)
from georiviere.river.models import Stream
from mapentity.registry import registry


class LangConverter(converters.StringConverter):
    # TODO: move this on geotrek to work with
    regex = '[a-z]{2}'


register_converter(LangConverter, 'lang')


app_name = 'river'


class StreamEntityOptions(AltimetryEntityOptions):
    document_view = StreamDocumentReport
    document_report_view = StreamDocumentReport

    def scan_views(self, *args, **kwargs):
        """ Adds the URLs of all views provided by ``PublishableMixin`` models.
        """
        views = super().scan_views(*args, **kwargs)
        publishable_views = [
            path('api/<lang:lang>/{name}s/<int:pk>/<slug:slug>.pdf'.format(name=self.modelname),
                 self.document_report_view.as_view(model=self.model),
                 name="%s_printable" % self.modelname),
        ]
        return publishable_views + views


urlpatterns = [
    path('cut_topology/', CutTopologyView.as_view(), name='cut_topology'),
    path('distance_to_source', DistanceToSourceView.as_view(), name='distance_to_source'),
    path('api/<lang:lang>/streams/<int:pk>/usages.geojson',
         StreamUsageViewSet.as_view({'get': 'list'}),
         name="stream_usage_geojson"),
    path('api/<lang:lang>/streams/<int:pk>/studies.geojson',
         StreamStudyViewSet.as_view({'get': 'list'}),
         name="stream_study_geojson"),
]
urlpatterns += registry.register(Stream, StreamEntityOptions)
