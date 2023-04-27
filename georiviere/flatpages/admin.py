from django.contrib import admin

from georiviere.flatpages import models as flatpages_models
from georiviere.flatpages.forms import FlatPageForm, FlatPagePictureFormSet


class FlatPagePictureAdminInline(admin.TabularInline):
    model = flatpages_models.FlatPagePicture
    extra = 1
    formset = FlatPagePictureFormSet

    def get_formset(self, request, obj=None, **kwargs):
        AdminFormSet = super(FlatPagePictureAdminInline, self).get_formset(request, obj, **kwargs)

        class AdminFormWithRequest(AdminFormSet):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return AdminFormSet(*args, **kwargs)

        return AdminFormWithRequest


class FlatPagesAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_filter = ('portals',)
    search_fields = ('title', 'content', 'external_url')
    form = FlatPageForm
    inlines = [
        FlatPagePictureAdminInline
    ]

    class Media:
        js = (
            '//cdnjs.cloudflare.com/ajax/libs/tinymce/4.1.2/tinymce.min.js',  # tinymce js file
            'js/tinymce.js',
        )


admin.site.register(flatpages_models.FlatPage, FlatPagesAdmin)
