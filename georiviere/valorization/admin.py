from django.contrib import admin

from georiviere.valorization.models import POICategory, POIType


class POITypeAdmin(admin.ModelAdmin):
    list_display = ('label',)
    search_fields = ('label',)


class POICategoryAdmin(admin.ModelAdmin):
    list_display = ('label',)
    search_fields = ('label',)


admin.site.register(POIType, POITypeAdmin)
admin.site.register(POICategory, POICategoryAdmin)
