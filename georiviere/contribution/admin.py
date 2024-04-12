from admin_ordering.admin import OrderableAdmin
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from leaflet.admin import LeafletGeoAdmin

from . import models, forms

admin.site.register(models.ContributionStatus, admin.ModelAdmin)
admin.site.register(models.SeverityType, admin.ModelAdmin)
admin.site.register(models.LandingType, admin.ModelAdmin)
admin.site.register(models.JamType, admin.ModelAdmin)
admin.site.register(models.DiseaseType, admin.ModelAdmin)
admin.site.register(models.DeadSpecies, admin.ModelAdmin)
admin.site.register(models.InvasiveSpecies, admin.ModelAdmin)
admin.site.register(models.HeritageSpecies, admin.ModelAdmin)
admin.site.register(models.HeritageObservation, admin.ModelAdmin)
admin.site.register(models.FishSpecies, admin.ModelAdmin)
admin.site.register(models.NaturePollution, admin.ModelAdmin)
admin.site.register(models.TypePollution, admin.ModelAdmin)


class CustomFieldInline(OrderableAdmin, admin.TabularInline):
    verbose_name = _('Field')
    verbose_name_plural = _('Fields')
    model = models.CustomContributionTypeField
    ordering_field = "order"
    ordering = ('order', 'label')
    form = forms.CustomContributionFieldForm
    fields = ('label', 'value_type', 'required', 'help_text',  'order')
    extra = 0
    show_change_link = True
    popup_link = 'change'


@admin.register(models.CustomContributionType)
class CustomContributionTypeAdmin(admin.ModelAdmin):
    list_display = ('label', )
    search_fields = ('label', )
    filter_horizontal = ('stations', )
    inlines = [CustomFieldInline, ]


@admin.register(models.CustomContributionTypeField)
class CustomContributionTypeFieldAdmin(admin.ModelAdmin):
    list_display = ('label', 'key', 'value_type', 'required', 'custom_type')
    list_filter = ('custom_type', 'value_type', 'required')
    search_fields = ('label', 'key', 'custom_type__label')
    form = forms.CustomContributionFieldForm
    fieldsets = (
        (None, {
            'fields': ('custom_type', 'label', 'key', 'value_type', 'required', 'help_text', 'order')
        }),
        (_('Customization'), {
            'fields': ('customization', 'options'),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.pk:
            return ['custom_type', 'value_type', 'key', 'options']
        return []

    def has_add_permission(self, request):
        """ Disable addition in list view """
        return False

    def has_delete_permission(self, request, obj=None):
        """ Disable deletion in list view """
        return False

@admin.register(models.CustomContribution)
class CustomContributionAdmin(LeafletGeoAdmin, admin.ModelAdmin):
    list_display = ('custom_type', 'portal', 'validated', 'date_insert', 'date_update')
    list_filter = ('custom_type', 'portal', 'validated')
    form = forms.CustomContributionForm

    def get_readonly_fields(self, request, obj=None):
        if not obj or not obj.pk:
            return ('data', )
        return []
