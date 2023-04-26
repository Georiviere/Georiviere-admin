from django.contrib import admin

from georiviere.flatpages import models as flatpages_models
from georiviere.flatpages.forms import FlatPageForm, FlatPagePictureForm


class FlatPagePictureAdminInline(admin.TabularInline):
    model = flatpages_models.FlatPagePicture
    extra = 1
    form = FlatPagePictureForm


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
