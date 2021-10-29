from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from georiviere.maintenance.models import (
    InterventionStatus, InterventionType,
    InterventionDisorder, InterventionStake,
    Intervention
)

admin.site.register(Intervention, LeafletGeoAdmin)
admin.site.register(InterventionType, admin.ModelAdmin)
admin.site.register(InterventionDisorder, admin.ModelAdmin)
admin.site.register(InterventionStake, admin.ModelAdmin)
admin.site.register(InterventionStatus, admin.ModelAdmin)
