from django.contrib import admin
from georiviere.observations.models import (
    Parameter,
    ParameterCategory,
    StationProfile,
    Unit,
)


class UnitAdmin(admin.ModelAdmin):
    list_display = ('code', 'label')
    search_fields = ('code', 'label')


class ParameterAdmin(admin.ModelAdmin):
    list_display = ('label', 'parameter_type')
    search_fields = ('label',)


admin.site.register(StationProfile)
admin.site.register(Unit, UnitAdmin)
admin.site.register(ParameterCategory)
admin.site.register(Parameter, ParameterAdmin)
