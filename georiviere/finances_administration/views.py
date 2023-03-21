from django.views import generic as generic_views
from django.utils.translation import gettext_lazy as _

from mapentity import views as mapentity_views
from geotrek.authent.decorators import same_structure_required
from rest_framework import permissions as rest_permissions

from georiviere.main.views import FormsetMixin
from georiviere.finances_administration.models import AdministrativeFile, AdministrativeOperation
from georiviere.finances_administration.filters import AdministrativeFileFilterSet
from georiviere.finances_administration.forms import (
    AdministrativeFileForm, AdministrativeOperationFormset, FundingFormSet,
    ManDayFormSet, AdministrativeOperationCostsForm
)
from georiviere.finances_administration.serializers import AdministrativeFileSerializer, AdministrativeFileGeojsonSerializer


class AdministrativeOperationOnObjectMixin(object):
    def form_valid(self, form):
        obj = self.get_object()
        if form.is_valid():
            if form.cleaned_data['administrative_file']:
                if isinstance(form.cleaned_data['administrative_file'], AdministrativeFile):
                    AdministrativeOperation.objects.create(content_type_id=obj.get_content_type_id(),
                                                           object_id=obj.pk,
                                                           administrative_file=form.cleaned_data['administrative_file'])
                else:
                    return self.form_invalid(form)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context['existing_administrative_files'] = AdministrativeFile.objects.prefetch_related('operations').filter(
            operations__content_type_id=obj.get_content_type_id(), operations__object_id=obj.pk).distinct()
        return context


class AdministrativeFileFormsetMixin:

    def form_valid(self, form):
        context = self.get_context_data()
        funding_formset = context['funding_formset']
        adminoperation_formset = context['adminoperation_formset']

        if form.is_valid():
            administrative_file = form.save()
            if funding_formset.is_valid():
                funding_formset.instance = administrative_file
                funding_formset.save()
            else:
                return self.form_invalid(form)
            if adminoperation_formset.is_valid():
                adminoperation_formset.instance = administrative_file
                adminoperation_formset.save()
            else:
                return self.form_invalid(form)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['funding_formset'] = FundingFormSet(
                self.request.POST,
                instance=self.object
            )
            context['adminoperation_formset'] = AdministrativeOperationFormset(
                self.request.POST,
                instance=self.object
            )
        else:
            context['funding_formset'] = FundingFormSet(
                instance=self.object
            )
            context['adminoperation_formset'] = AdministrativeOperationFormset(
                instance=self.object
            )
        return context


class AdministrativeFileList(mapentity_views.MapEntityList):
    queryset = AdministrativeFile.objects.all()
    filterform = AdministrativeFileFilterSet
    columns = ['id', 'name']


class AdministrativeFileLayer(mapentity_views.MapEntityLayer):
    queryset = AdministrativeFile.objects.all()
    model = AdministrativeFile
    properties = ['name']

    def get_queryset(self):
        return super().get_queryset()


class AdministrativeFileJsonList(mapentity_views.MapEntityJsonList, AdministrativeFileList):
    pass


class AdministrativeFileFormat(mapentity_views.MapEntityFormat, AdministrativeFileList):
    queryset = AdministrativeFile.objects.all()


class AdministrativeFileDocumentOdt(mapentity_views.MapEntityDocumentOdt):
    queryset = AdministrativeFile.objects.all()


class AdministrativeFileDocumentWeasyprint(mapentity_views.MapEntityDocumentWeasyprint):
    queryset = AdministrativeFile.objects.all()


class AdministrativeFileDetail(mapentity_views.MapEntityDetail):
    queryset = AdministrativeFile.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['can_edit'] = self.get_object().same_structure(self.request.user)
        return context


class AdministrativeFileCreate(AdministrativeFileFormsetMixin, mapentity_views.MapEntityCreate):
    model = AdministrativeFile
    form_class = AdministrativeFileForm


class AdministrativeFileUpdate(AdministrativeFileFormsetMixin, mapentity_views.MapEntityUpdate):
    model = AdministrativeFile
    form_class = AdministrativeFileForm

    @same_structure_required('finances_administration:administrativefile_detail')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class AdministrativeFileDelete(mapentity_views.MapEntityDelete):
    model = AdministrativeFile

    @same_structure_required('finances_administration:administrativefile_detail')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class AdministrativeFileViewSet(mapentity_views.MapEntityViewSet):
    model = AdministrativeFile
    queryset = AdministrativeFile.objects.all()
    serializer_class = AdministrativeFileSerializer
    geojson_serializer_class = AdministrativeFileGeojsonSerializer
    permission_classes = [rest_permissions.DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        # Override annotation done by MapEntityViewSet.get_queryset()
        return AdministrativeFile.objects.all()


class ManDayFormSet(FormsetMixin):
    context_name = "manday_formset"
    formset_class = ManDayFormSet


class AdministrativeOperationUpdate(ManDayFormSet, generic_views.UpdateView):
    model = AdministrativeOperation
    form_class = AdministrativeOperationCostsForm

    def get_title(self):
        return _("Edit costs for").format(self.get_object())

    def get_success_url(self):
        return self.get_object().administrative_file.get_detail_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_title()
        return context
