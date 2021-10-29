from django.contrib import admin

from leaflet.admin import LeafletGeoAdmin

from georiviere.watershed.models import Watershed, WatershedType


class WatershedTypeAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name',)
    merge_field = 'name'


class WatershedAdmin(LeafletGeoAdmin):
    search_fields = ('name',)
    list_display = ('name', 'watershed_type')
    list_filter = ('watershed_type', )


admin.site.register(WatershedType, WatershedTypeAdmin)
admin.site.register(Watershed, WatershedAdmin)
