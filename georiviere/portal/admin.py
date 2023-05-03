from django.contrib import admin

from leaflet.admin import LeafletGeoAdmin

from georiviere.portal.models import MapBaseLayer, MapOverlayLayer, MapOverlayGroupLayer, Portal


class PortalAdmin(LeafletGeoAdmin, admin.ModelAdmin):
    list_display = ('name', 'website', 'title')
    search_fields = ('name', 'website')


class MapBaseLayerAdmin(admin.ModelAdmin):
    list_display = ('label', 'url')
    search_fields = ('label', )


class MapOverlayGroupLayerAdmin(admin.ModelAdmin):
    list_display = ('label', )
    search_fields = ('label', )


class MapOverlayLayerAdmin(admin.ModelAdmin):
    list_display = ('label', 'url')
    search_fields = ('label', )


admin.site.register(Portal, PortalAdmin)
admin.site.register(MapBaseLayer, MapBaseLayerAdmin)
admin.site.register(MapOverlayGroupLayer, MapOverlayGroupLayerAdmin)
admin.site.register(MapOverlayLayer, MapOverlayLayerAdmin)
