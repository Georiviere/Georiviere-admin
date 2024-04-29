from admin_ordering.admin import OrderableAdmin
from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models import FileField
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from leaflet.admin import LeafletGeoAdmin

from . import models, forms
from ..main.models import Attachment

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
    verbose_name = _("Field")
    verbose_name_plural = _("Fields")
    model = models.CustomContributionTypeField
    ordering_field = "order"
    ordering = ("order", "label")
    form = forms.CustomContributionFieldInlineForm
    fields = (
        "label",
        "internal_identifier",
        "value_type",
        "required",
        "help_text",
        "order",
    )
    extra = 0
    show_change_link = True
    popup_link = "change"


@admin.register(models.CustomContributionType)
class CustomContributionTypeAdmin(admin.ModelAdmin):
    list_display = ("label",)
    search_fields = ("label",)
    filter_horizontal = ("stations",)
    inlines = [
        CustomFieldInline,
    ]


@admin.register(models.CustomContributionTypeField)
class CustomContributionTypeFieldAdmin(admin.ModelAdmin):
    list_display = ("label", "key", "value_type", "required", "custom_type")
    list_filter = ("custom_type", "value_type", "required")
    search_fields = ("label", "key", "custom_type__label")
    form = forms.CustomContributionFieldForm
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "custom_type",
                    "label",
                    "internal_identifier",
                    "key",
                    "value_type",
                    "required",
                    "help_text",
                )
            },
        ),
        (
            _("Customization"),
            {
                "fields": ("customization", "options"),
            },
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.pk:
            return ["custom_type", "key", "options"]
        return []

    def has_add_permission(self, request):
        """Disable addition in list view"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Disable deletion in list view"""
        return False


class AdminImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            file_name = str(value)
            output.append(
                ' <a href="%s" target="_blank"><img src="%s" alt="%s" style="max-height: 60px; max-width: 60px;"/></a> %s '
                % (image_url, image_url, file_name, _(""))
            )
        output.append(super().render(name, value, attrs))
        return mark_safe("".join(output))


class CustomContribAttachmentInline(GenericTabularInline):
    model = Attachment
    extra = 0
    exclude = ("attachment_video", "attachment_link", "creator", "legend", "starred")
    formfield_overrides = {FileField: {"widget": AdminImageWidget}}


@admin.register(models.CustomContribution)
class CustomContributionAdmin(LeafletGeoAdmin, admin.ModelAdmin):
    list_display = ("custom_type", "portal", "validated", "date_insert", "date_update")
    list_filter = ("custom_type", "portal", "validated")
    form = forms.CustomContributionForm
    inlines = [CustomContribAttachmentInline]

    def get_readonly_fields(self, request, obj=None):
        if not obj or not obj.pk:
            return ("data",)
        return []
