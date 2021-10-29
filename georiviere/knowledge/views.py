from mapentity import views as mapentity_views
from geotrek.authent.decorators import same_structure_required
from rest_framework import permissions as rest_permissions

from georiviere.knowledge.filters import KnowledgeFilterSet, FollowUpFilterSet
from georiviere.knowledge.forms import KnowledgeForm, VegetationForm, WorkForm, FollowUpForm
from georiviere.knowledge.models import Knowledge, KnowledgeType, FollowUp
from georiviere.knowledge.serializers import FollowUpSerializer, FollowUpGeojsonSerializer


class VegetationWorkFormMixin(object):
    """Mixin view to insert vegetation or work form according to knowledge type"""
    vegetation_form_class = VegetationForm
    work_form_class = WorkForm

    def form_valid(self, form):
        context = self.get_context_data()
        if form.is_valid():
            if form.cleaned_data['knowledge_type'] == KnowledgeType.objects.get(id=1):
                vegetation_form = context['vegetation_form']
                if vegetation_form.is_valid():
                    knowledge = form.save()
                    vegetation_form.instance.knowledge = knowledge
                    vegetation_form.save()
                else:
                    return self.form_invalid(form)
            if form.cleaned_data['knowledge_type'] == KnowledgeType.objects.get(id=2):
                work_form = context['work_form']
                if work_form.is_valid():
                    knowledge = form.save()
                    work_form.instance.knowledge = knowledge
                    work_form.save()
                else:
                    return self.form_invalid(form)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['vegetation_form'] = VegetationForm(self.request.POST)
            context['work_form'] = WorkForm(self.request.POST)
            if self.object and hasattr(self.object, "vegetation"):
                context['vegetation_form'] = VegetationForm(
                    self.request.POST,
                    instance=self.object.vegetation,
                )
            if self.object and hasattr(self.object, "work"):
                context['work_form'] = WorkForm(
                    self.request.POST,
                    instance=self.object.work,
                )
        else:
            context['vegetation_form'] = VegetationForm()
            context['work_form'] = WorkForm()
            if self.object and hasattr(self.object, "vegetation"):
                context['vegetation_form'] = VegetationForm(instance=self.object.vegetation,)
            if self.object and hasattr(self.object, "work"):
                context['work_form'] = WorkForm(instance=self.object.work)
        return context


class KnowledgeList(mapentity_views.MapEntityList):
    queryset = Knowledge.objects.select_related('knowledge_type').all()
    filterform = KnowledgeFilterSet
    columns = ['id', 'name', 'knowledge_type']


class KnowledgeLayer(mapentity_views.MapEntityLayer):
    queryset = Knowledge.objects.select_related('knowledge_type').all()
    model = Knowledge


class KnowledgeJsonList(mapentity_views.MapEntityJsonList, KnowledgeList):
    pass


class KnowledgeFormat(mapentity_views.MapEntityFormat):
    queryset = Knowledge.objects\
        .select_related('structure', 'knowledge_type').all()


class KnowledgeDocumentOdt(mapentity_views.MapEntityDocumentOdt):
    model = Knowledge


class KnowledgeDocumentWeasyprint(mapentity_views.MapEntityDocumentWeasyprint):
    model = Knowledge


class KnowledgeDetail(mapentity_views.MapEntityDetail):
    queryset = Knowledge.objects\
        .select_related('structure', 'knowledge_type', 'vegetation', 'work').all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['can_edit'] = self.get_object().same_structure(self.request.user)
        return context


class KnowledgeCreate(VegetationWorkFormMixin, mapentity_views.MapEntityCreate):
    model = Knowledge
    form_class = KnowledgeForm


class KnowledgeUpdate(VegetationWorkFormMixin, mapentity_views.MapEntityUpdate):
    model = Knowledge
    form_class = KnowledgeForm

    @same_structure_required('knowledge:knowledge_detail')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class KnowledgeDelete(mapentity_views.MapEntityDelete):
    model = Knowledge

    @same_structure_required('knowledge:knowledge_detail')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class FollowUpList(mapentity_views.MapEntityList):
    queryset = FollowUp.objects.select_related('followup_type').all()
    filterform = FollowUpFilterSet
    columns = ['id', 'name', 'date', 'followup_type']


class FollowUpLayer(mapentity_views.MapEntityLayer):
    queryset = FollowUp.objects.select_related('followup_type').all()
    model = FollowUp
    filterform = FollowUpFilterSet
    properties = ['name']

    def get_queryset(self):
        return super().get_queryset()


class FollowUpJsonList(mapentity_views.MapEntityJsonList, FollowUpList):
    pass


class FollowUpFormat(mapentity_views.MapEntityFormat):
    queryset = FollowUp.objects\
        .select_related('structure', 'followup_type', 'knowledge').all()
    filterform = FollowUpFilterSet


class FollowUpDocumentOdt(mapentity_views.MapEntityDocumentOdt):
    queryset = FollowUp.objects\
        .select_related('followup_type', 'knowledge').all()


class FollowUpDocumentWeasyprint(mapentity_views.MapEntityDocumentWeasyprint):
    queryset = FollowUp.objects\
        .select_related('followup_type', 'knowledge').all()


class FollowUpDetail(mapentity_views.MapEntityDetail):
    queryset = FollowUp.objects\
        .select_related('structure', 'followup_type', 'knowledge').all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['can_edit'] = self.get_object().same_structure(self.request.user)
        return context


class FollowUpCreate(mapentity_views.MapEntityCreate):
    model = FollowUp
    form_class = FollowUpForm


class FollowUpUpdate(mapentity_views.MapEntityUpdate):
    model = FollowUp
    form_class = FollowUpForm

    @same_structure_required('knowledge:followup_detail')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class FollowUpDelete(mapentity_views.MapEntityDelete):
    model = FollowUp

    @same_structure_required('knowledge:followup_detail')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class FollowUpViewSet(mapentity_views.MapEntityViewSet):
    model = FollowUp
    queryset = FollowUp.objects\
        .select_related('followup_type', 'knowledge').all()
    serializer_class = FollowUpSerializer
    geojson_serializer_class = FollowUpGeojsonSerializer
    permission_classes = [rest_permissions.DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        # Override annotation done by MapEntityViewSet.get_queryset()
        return FollowUp.objects\
            .select_related('followup_type', 'knowledge').all()
