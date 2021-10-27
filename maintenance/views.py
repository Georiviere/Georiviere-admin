from mapentity import views as mapentity_views
from geotrek.authent.decorators import same_structure_required
from rest_framework import permissions as rest_permissions

from maintenance.models import Intervention
from maintenance.forms import InterventionForm
from maintenance.filters import InterventionFilterSet
from maintenance.serializers import InterventionSerializer, InterventionGeojsonSerializer


class InterventionList(mapentity_views.MapEntityList):
    model = Intervention
    filterform = InterventionFilterSet
    columns = ['id', 'name', 'date', 'intervention_type', 'intervention_status', 'target']


class InterventionLayer(mapentity_views.MapEntityLayer):
    queryset = Intervention.objects.all()
    model = Intervention
    filterform = InterventionFilterSet
    properties = ['name']

    def get_queryset(self):
        return super().get_queryset()


class InterventionJsonList(mapentity_views.MapEntityJsonList, InterventionList):
    pass


class InterventionFormat(mapentity_views.MapEntityFormat):
    model = Intervention
    filterform = InterventionFilterSet


class InterventionDocumentOdt(mapentity_views.MapEntityDocumentOdt):
    model = Intervention


class InterventionDocumentWeasyprint(mapentity_views.MapEntityDocumentWeasyprint):
    model = Intervention


class InterventionDetail(mapentity_views.MapEntityDetail):
    queryset = Intervention.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['can_edit'] = self.get_object().same_structure(self.request.user)
        return context


class InterventionCreate(mapentity_views.MapEntityCreate):
    model = Intervention
    form_class = InterventionForm


class InterventionUpdate(mapentity_views.MapEntityUpdate):
    model = Intervention
    form_class = InterventionForm

    @same_structure_required('maintenance:intervention_detail')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class InterventionDelete(mapentity_views.MapEntityDelete):
    model = Intervention

    @same_structure_required('maintenance:intervention_detail')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class InterventionViewSet(mapentity_views.MapEntityViewSet):
    model = Intervention
    queryset = Intervention.objects.all()
    serializer_class = InterventionSerializer
    geojson_serializer_class = InterventionGeojsonSerializer
    permission_classes = [rest_permissions.DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        # Override annotation done by MapEntityViewSet.get_queryset()
        return Intervention.objects.all()
