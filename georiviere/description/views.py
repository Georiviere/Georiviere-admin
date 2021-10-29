from mapentity import views as mapentity_views

from geotrek.authent.decorators import same_structure_required
from .filters import UsageFilterSet, StatusFilterSet, LandFilterSet, MorphologyFilterSet
from .forms import LandForm, MorphologyForm, UsageForm, StatusForm
from .models import Land, Morphology, Status, Usage
from georiviere.river.views import TopologyAddDeleteMixin, TopologyUpdateMixin, TopologyListMixin
from georiviere.river.decorators import same_structure_topology_required


class LandList(mapentity_views.MapEntityList):
    model = Land
    filterform = LandFilterSet
    columns = ['id', 'land_type', 'length']


class LandLayer(mapentity_views.MapEntityLayer):
    model = Land
    properties = ['land_type', ]


class LandJsonList(mapentity_views.MapEntityJsonList, LandList):
    pass


class LandFormat(mapentity_views.MapEntityFormat, LandList):
    model = Land


class LandDocumentOdt(mapentity_views.MapEntityDocumentOdt):
    model = Land


class LandDocumentWeasyprint(mapentity_views.MapEntityDocumentWeasyprint):
    model = Land


class LandDetail(mapentity_views.MapEntityDetail):
    model = Land

    def get_context_data(self, *args, **kwargs):
        context = super(LandDetail, self).get_context_data(*args, **kwargs)
        context['can_edit'] = self.get_object().same_structure(self.request.user)
        return context


class LandCreate(mapentity_views.MapEntityCreate):
    model = Land
    form_class = LandForm


class LandUpdate(mapentity_views.MapEntityUpdate):
    model = Land
    form_class = LandForm

    @same_structure_required('description:land_detail')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class LandDelete(mapentity_views.MapEntityDelete):
    model = Land

    @same_structure_required('description:land_detail')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class UsageList(mapentity_views.MapEntityList):
    model = Usage
    filterform = UsageFilterSet
    columns = ['id', 'usage_types', 'length']


class UsageLayer(mapentity_views.MapEntityLayer):
    model = Usage
    properties = ['usage_types', ]


class UsageJsonList(mapentity_views.MapEntityJsonList, UsageList):
    pass


class UsageFormat(mapentity_views.MapEntityFormat, UsageList):
    model = Usage


class UsageDocumentOdt(mapentity_views.MapEntityDocumentOdt):
    model = Usage


class UsageDocumentWeasyprint(mapentity_views.MapEntityDocumentWeasyprint):
    model = Usage


class UsageDetail(mapentity_views.MapEntityDetail):
    model = Usage

    def get_context_data(self, *args, **kwargs):
        context = super(UsageDetail, self).get_context_data(*args, **kwargs)
        context['can_edit'] = self.get_object().same_structure(self.request.user)
        return context


class UsageCreate(mapentity_views.MapEntityCreate):
    model = Usage
    form_class = UsageForm


class UsageUpdate(mapentity_views.MapEntityUpdate):
    model = Usage
    form_class = UsageForm

    @same_structure_required('description:usage_detail')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class UsageDelete(mapentity_views.MapEntityDelete):
    model = Usage

    @same_structure_required('description:usage_detail')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class MorphologyList(TopologyListMixin, mapentity_views.MapEntityList):
    model = Morphology
    filterform = MorphologyFilterSet
    columns = ['id', 'name']


class MorphologyLayer(mapentity_views.MapEntityLayer):
    model = Morphology
    properties = ['good_working_space_left', 'good_working_space_right', 'facies_diversity', 'main_flow',
                  'secondary_flow', 'granulometric_diversity', 'full_edge_height', 'full_edge_width',
                  'sediment_dynamic', 'bank_state_left', 'bank_state_right', 'habitats_diversity', 'main_habitat',
                  'secondary_habitat', 'plan_layout']


class MorphologyJsonList(mapentity_views.MapEntityJsonList, MorphologyList):
    pass


class MorphologyFormat(mapentity_views.MapEntityFormat, MorphologyList):
    model = Morphology


class MorphologyDocumentOdt(mapentity_views.MapEntityDocumentOdt):
    model = Morphology


class MorphologyDocumentWeasyprint(mapentity_views.MapEntityDocumentWeasyprint):
    model = Morphology


class MorphologyDetail(mapentity_views.MapEntityDetail):
    model = Morphology


class MorphologyCreate(TopologyAddDeleteMixin, mapentity_views.MapEntityCreate):
    model = Morphology
    form_class = MorphologyForm


class MorphologyUpdate(TopologyUpdateMixin, mapentity_views.MapEntityUpdate):
    model = Morphology
    form_class = MorphologyForm

    @same_structure_topology_required('description:morphology_detail')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class MorphologyDelete(TopologyAddDeleteMixin, mapentity_views.MapEntityDelete):
    model = Morphology


class StatusList(TopologyListMixin, mapentity_views.MapEntityList):
    model = Status
    filterform = StatusFilterSet
    columns = ['id', 'status_types', 'length']


class StatusLayer(mapentity_views.MapEntityLayer):
    model = Status
    properties = ['status_types', ]


class StatusJsonList(mapentity_views.MapEntityJsonList, StatusList):
    pass


class StatusFormat(mapentity_views.MapEntityFormat, StatusList):
    model = Status


class StatusDocumentOdt(mapentity_views.MapEntityDocumentOdt):
    model = Status


class StatusDocumentWeasyprint(mapentity_views.MapEntityDocumentWeasyprint):
    model = Status


class StatusDetail(mapentity_views.MapEntityDetail):
    model = Status


class StatusCreate(TopologyAddDeleteMixin, mapentity_views.MapEntityCreate):
    model = Status
    form_class = StatusForm


class StatusUpdate(TopologyUpdateMixin, mapentity_views.MapEntityUpdate):
    model = Status
    form_class = StatusForm

    @same_structure_topology_required('description:status_detail')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class StatusDelete(TopologyAddDeleteMixin, mapentity_views.MapEntityDelete):
    model = Status
