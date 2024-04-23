from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from mapentity.registry import registry
from mapentity import views as mapentity_views


def handler500(request, *args, **kwargs):
    return HttpResponse(status=500)


@login_required(login_url='login')
def home(request):
    last = request.session.get('last_list')  # set in MapEntityList
    for entity in registry.entities:
        if reverse(entity.url_list) == last and request.user.has_perm(entity.model.get_permission_codename('list')):
            return redirect(entity.url_list)
    for entity in registry.entities:
        if entity.menu and request.user.has_perm(entity.model.get_permission_codename('list')):
            return redirect(entity.url_list)
    return redirect('river:river_list')


class JSSettings(mapentity_views.JSSettings):
    def get_context_data(self):
        dictsettings = super().get_context_data()
        dictsettings['map'].update(
            snap_distance=settings.SNAP_DISTANCE
        )
        return dictsettings


class FormsetMixin:
    """Mixin for Formset to be used in Mapentity forms
    WARNING: this will only work for a single formset in form
    TODO: move this to Mapentity
    """
    context_name = None
    formset_class = None

    def form_valid(self, form):
        context = self.get_context_data()
        formset_form = context[self.context_name]

        if formset_form.is_valid():
            response = super().form_valid(form)
            formset_form.instance = self.object
            formset_form.save()
        else:
            response = self.form_invalid(form)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context[self.context_name] = self.formset_class(
                self.request.POST, instance=self.object)
        else:
            context[self.context_name] = self.formset_class(
                instance=self.object)
        return context
