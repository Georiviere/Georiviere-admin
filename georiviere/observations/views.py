from mapentity import views as mapentity_views
from geotrek.authent.decorators import same_structure_required

from georiviere.finances_administration.views import AdministrativeOperationOnObjectMixin
from georiviere.main.views import FormsetMixin
from .filters import StationFilterSet
from .forms import StationForm, ParameterTrackingFormset
from .models import Station


class ParameterTrackingFormsetMixin(FormsetMixin):
    context_name = "parametertracking_formset"
    formset_class = ParameterTrackingFormset


class StationList(mapentity_views.MapEntityList):
    queryset = Station.objects\
        .prefetch_related('station_profiles').all()
    filterform = StationFilterSet
    columns = ['id', 'code', 'label']


class StationLayer(mapentity_views.MapEntityLayer):
    model = Station


class StationJsonList(mapentity_views.MapEntityJsonList, StationList):
    pass


class StationFormat(mapentity_views.MapEntityFormat, StationList):
    model = Station


class StationDocumentOdt(mapentity_views.MapEntityDocumentOdt):
    model = Station


class StationDocumentWeasyprint(mapentity_views.MapEntityDocumentWeasyprint):
    model = Station


class StationDetail(mapentity_views.MapEntityDetail):
    queryset = Station.objects\
        .select_related('structure').all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['can_edit'] = self.get_object().same_structure(self.request.user)
        return context


class StationCreate(AdministrativeOperationOnObjectMixin, ParameterTrackingFormsetMixin, mapentity_views.MapEntityCreate):
    model = Station
    form_class = StationForm


class StationUpdate(AdministrativeOperationOnObjectMixin, ParameterTrackingFormsetMixin, mapentity_views.MapEntityUpdate):
    model = Station
    form_class = StationForm

    @same_structure_required('observations:station_detail')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class StationDelete(mapentity_views.MapEntityDelete):
    model = Station

    @same_structure_required('observations:station_detail')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
