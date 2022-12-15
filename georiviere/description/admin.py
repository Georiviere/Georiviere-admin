from django.contrib import admin
from .models import (StatusType, LandType, UsageType, FlowType, WorkingSpaceType, FaciesDiversity,
                     GranulometricDiversity, SedimentDynamic, BankState, HabitatsDiversity, HabitatType, PlanLayoutType)
from geotrek.common.mixins.actions import MergeActionMixin


class PhysicalTypeAdmin(MergeActionMixin, admin.ModelAdmin):
    list_display = ('label',)
    search_fields = ('label', )
    merge_field = "label"


class LandTypeAdmin(MergeActionMixin, admin.ModelAdmin):
    list_display = ('label', )
    search_fields = ('label', )
    merge_field = "label"


class UsageTypeAdmin(MergeActionMixin, admin.ModelAdmin):
    list_display = ('label', )
    search_fields = ('label', )
    merge_field = "label"


class FlowTypeAdmin(MergeActionMixin, admin.ModelAdmin):
    list_display = ('label', )
    search_fields = ('label', )
    merge_field = "label"


class WorkingSpaceTypeAdmin(MergeActionMixin, admin.ModelAdmin):
    list_display = ('label', )
    search_fields = ('label', )
    merge_field = "label"


class FaciesDiversityAdmin(MergeActionMixin, admin.ModelAdmin):
    list_display = ('label', )
    search_fields = ('label', )
    merge_field = "label"


class GranulometricDiversityAdmin(MergeActionMixin, admin.ModelAdmin):
    list_display = ('label', )
    search_fields = ('label', )
    merge_field = "label"


class SedimentDynamicAdmin(MergeActionMixin, admin.ModelAdmin):
    list_display = ('label', )
    search_fields = ('label', )
    merge_field = "label"


class BankStateAdmin(MergeActionMixin, admin.ModelAdmin):
    list_display = ('label', )
    search_fields = ('label', )
    merge_field = "label"


class HabitatsDiversityAdmin(MergeActionMixin, admin.ModelAdmin):
    list_display = ('label', )
    search_fields = ('label', )
    merge_field = "label"


class HabitatTypeAdmin(MergeActionMixin, admin.ModelAdmin):
    list_display = ('label', )
    search_fields = ('label', )
    merge_field = "label"


class PlanLayoutTypeAdmin(MergeActionMixin, admin.ModelAdmin):
    list_display = ('label', )
    search_fields = ('label', )
    merge_field = "label"


admin.site.register(StatusType, PhysicalTypeAdmin)
admin.site.register(LandType, LandTypeAdmin)
admin.site.register(UsageType, UsageTypeAdmin)
admin.site.register(FlowType, FlowTypeAdmin)
admin.site.register(WorkingSpaceType, WorkingSpaceTypeAdmin)
admin.site.register(FaciesDiversity, FaciesDiversityAdmin)
admin.site.register(GranulometricDiversity, GranulometricDiversityAdmin)
admin.site.register(SedimentDynamic, SedimentDynamicAdmin)
admin.site.register(BankState, BankStateAdmin)
admin.site.register(HabitatsDiversity, HabitatsDiversityAdmin)
admin.site.register(HabitatType, HabitatTypeAdmin)
admin.site.register(PlanLayoutType, PlanLayoutTypeAdmin)
