from admin_ordering.admin import OrderableAdmin
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from leaflet.admin import LeafletGeoAdmin

from . import models
from .forms import CustomContributionForm

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
    extra = 0


@admin.register(models.CustomContributionType)
class CustomContributionTypeAdmin(admin.ModelAdmin):
    list_display = ('label', )
    search_fields = ('label', )
    inlines = [CustomFieldInline, ]


@admin.register(models.CustomContribution)
class CustomContributionAdmin(LeafletGeoAdmin, admin.ModelAdmin):
    list_display = ('custom_type', 'portal', 'validated', 'date_insert', 'date_update')
    list_filter = ('custom_type', 'portal', 'validated')
    form = CustomContributionForm

    def get_form(self, request, obj=None, change=False, **kwargs):
        extra_fields = {}
        if obj and obj.pk:
            for field in obj.custom_type.fields.all():
                initials = {}
                if field.key in obj.properties:
                    initials = {'initial': obj.properties.get(field.key)}
                form_field = field.get_form_field(**initials)
                extra_fields[field.key] = form_field
        form = super().get_form(request, obj, change, fields=extra_fields)
        return form

