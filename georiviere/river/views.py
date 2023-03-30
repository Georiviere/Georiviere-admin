from django.conf import settings
from django.contrib import messages
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Length, LineLocatePoint, Transform
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, F, FloatField, Case, Min, When
from django.db.utils import InternalError
from django.http import JsonResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from django.views.generic.edit import FormView
from django.views.generic.base import View
from geotrek.authent.decorators import same_structure_required

from georiviere.functions import ClosestPoint, LineSubString
from .forms import CutTopologyForm, StreamForm
from .models import Stream, Topology
from .filters import StreamFilterSet
from georiviere.main.mixins.views import DocumentReportMixin
from georiviere.description.models import Status, StatusType, Usage
from georiviere.description.serializers import UsageAPIGeojsonSerializer
from georiviere.studies.models import Study
from georiviere.studies.serializers import StudyAPIGeojsonSerializer


from mapentity import views as mapentity_views

from rest_framework import permissions as rest_permissions, viewsets


class StreamList(mapentity_views.MapEntityList):
    queryset = Stream.objects.all()
    columns = ['id', 'name', 'length']
    filterform = StreamFilterSet


class StreamLayer(mapentity_views.MapEntityLayer):
    queryset = Stream.objects.select_related('classification_water_policy')


class StreamJsonList(mapentity_views.MapEntityJsonList, StreamList):
    pass


class StreamUsageViewSet(viewsets.ModelViewSet):
    model = Usage
    serializer_class = UsageAPIGeojsonSerializer
    permission_classes = [rest_permissions.DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        pk = self.kwargs['pk']
        stream = get_object_or_404(Stream.objects.all(), pk=pk)
        return stream.usages.annotate(api_geom=Transform("geom", settings.API_SRID)).prefetch_related('usage_types',)


class StreamStudyViewSet(viewsets.ModelViewSet):
    model = Study
    serializer_class = StudyAPIGeojsonSerializer
    permission_classes = [rest_permissions.DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        pk = self.kwargs['pk']
        stream = get_object_or_404(Stream.objects.all(), pk=pk)
        return stream.studies.annotate(api_geom=Transform("geom", settings.API_SRID))


class StreamDocumentReport(DocumentReportMixin, mapentity_views.MapEntityDocumentWeasyprint):
    def get_context_data(self, *args, **kwargs):
        rooturl = self.request.build_absolute_uri('/')
        self.get_object().prepare_map_image_with_other_objects(rooturl, ["usages"])
        self.get_object().prepare_map_image_with_other_objects(rooturl, ["studies"])
        context = super(StreamDocumentReport, self).get_context_data(*args, **kwargs)
        topologies = Topology.objects.filter(stream=self.get_object())
        status_types = {}
        for status_type in StatusType.objects.filter(status__in=Status.objects.filter(
                topology__in=topologies.filter(status__isnull=False).values_list('pk', flat=True)).values_list('pk',
                                                                                                               flat=True)):
            infos = status_type.status.annotate(length_2d=Length('geom')).aggregate(sum_length=Sum('length_2d'),
                                                                                    percentage=Sum(
                                                                                        F('topology__end_position') - F(
                                                                                            'topology__start_position')) * 100)
            status_types[status_type.label] = infos
        context['status_types'] = status_types
        context['map_path_usage'] = self.get_object().get_map_image_path_with_other_objects(["usages"])
        context['map_path_study'] = self.get_object().get_map_image_path_with_other_objects(["studies"])
        return context

    @property
    def status_type_on_stream(self):
        topologies = Topology.objects.filter(stream=self)
        return topologies.filter(status__isnull=False)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not self.request.user.is_authenticated:
            raise PermissionDenied
        if not self.request.user.has_perm('%s.read_%s' % (obj._meta.app_label, obj._meta.model_name)):
            raise PermissionDenied
        return obj


class StreamFormat(mapentity_views.MapEntityFormat):
    queryset = Stream.objects.all()


class StreamDocumentOdt(mapentity_views.MapEntityDocumentOdt):
    queryset = Stream.objects.all()


class StreamDocumentWeasyprint(mapentity_views.MapEntityDocumentWeasyprint):
    queryset = Stream.objects.all()


class StreamDetail(mapentity_views.MapEntityDetail):
    queryset = Stream.objects.all()

    @property
    def icon_sizes(self):
        return {
            'source': settings.ICON_SIZES['river_source'],
        }

    def get_context_data(self, *args, **kwargs):
        context = super(StreamDetail, self).get_context_data(*args, **kwargs)
        context['can_edit'] = self.get_object().same_structure(self.request.user)
        return context


class StreamCreate(mapentity_views.MapEntityCreate):
    model = Stream
    form_class = StreamForm


class StreamUpdate(mapentity_views.MapEntityUpdate):
    model = Stream
    form_class = StreamForm

    @same_structure_required('river:stream_detail')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class StreamDelete(mapentity_views.MapEntityDelete):
    model = Stream

    @same_structure_required('river:stream_detail')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class TopologyUpdateMixin(object):
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['can_delete'] = False
        return kwargs


class TopologyListMixin(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_add'] = False
        return context


class TopologyAddDeleteMixin(object):
    def dispatch(self, *args, **kwargs):
        raise PermissionDenied


class CutTopologyView(LoginRequiredMixin, FormView):
    form_class = CutTopologyForm
    http_method_names = ['post']

    def form_valid(self, form):
        topology = form.cleaned_data['topology']
        if hasattr(topology, 'status'):
            instance = topology.status
        elif hasattr(topology, 'morphology'):
            instance = topology.morphology
        try:

            geom_point = Point(x=float(form.cleaned_data['lng']),
                               y=float(form.cleaned_data['lat']),
                               srid=4326).transform(settings.SRID, clone=True)
            topology_filter = instance.__class__.objects.filter(pk=instance.pk).annotate(locate_point=LineLocatePoint('geom', geom_point))
            locate_point = topology_filter.first().locate_point
            if locate_point == 0 or locate_point == 1:
                messages.error(self.request, _("Topology could not be cut"))
                return HttpResponseRedirect(instance.__class__.get_detail_url(instance))
        except InternalError:
            messages.error(self.request, _("Topology could not be cut"))
            return HttpResponseRedirect(instance.__class__.get_detail_url(instance))
        old_start_position = topology.start_position
        old_end_position = topology.end_position
        final_position = (old_end_position - old_start_position) * locate_point + old_start_position
        topology.start_position = final_position
        topology.save()

        new_topology = Topology.objects.create(start_position=old_start_position, end_position=final_position,
                                               stream=topology.stream)

        duplicate_instance = instance
        duplicate_instance.pk = None
        duplicate_instance.topology = new_topology
        duplicate_instance.save()
        new_topology.save()

        messages.success(self.request, _("Topology has been cut"))
        return HttpResponseRedirect(duplicate_instance.get_detail_url())


class DistanceToSourceView(LoginRequiredMixin, View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        geom_point = Point(x=float(request.GET['lng_distance']),
                           y=float(request.GET['lat_distance']),
                           srid=4326).transform(settings.SRID, clone=True)
        streams = Stream.objects.annotate(distance=Distance(
            F('geom'), geom_point, output_field=FloatField()))
        stream_min_distance = streams.aggregate(
            min_distance=Min(F('distance'))
        )['min_distance']
        streams = streams.annotate(locate_source=LineLocatePoint(F('geom'),
                                                                 F('source_location')),
                                   locate_point=LineLocatePoint(F('geom'),
                                                                ClosestPoint(F('geom'),
                                                                             geom_point)),
                                   locate=Length(LineSubString(
                                       F('geom'),
                                       Case(
                                           When(locate_source__gte=F('locate_point'),
                                                then=F('locate_point')),
                                           default=F('locate_source')
                                       ),
                                       Case(
                                           When(locate_source__gte=F('locate_point'),
                                                then=F('locate_source')),
                                           default=F('locate_point')
                                       ))) + F('distance') + Distance(F('geom'),
                                                                      F('source_location'),
                                                                      output_field=FloatField())
                                   ).filter(distance=stream_min_distance)

        return JsonResponse({"distance": round(streams.first().locate.m, 1) if streams else 0})
