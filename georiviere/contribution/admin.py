from django.contrib import admin

from georiviere.contribution.models import (
    SeverityType, LandingType, JamType, DiseaseType, DeadSpecies, InvasiveSpecies, HeritageSpecies, HeritageObservation,
    FishSpecies, NaturePollution, TypePollution
)

admin.site.register(SeverityType, admin.ModelAdmin)
admin.site.register(LandingType, admin.ModelAdmin)
admin.site.register(JamType, admin.ModelAdmin)
admin.site.register(DiseaseType, admin.ModelAdmin)
admin.site.register(DeadSpecies, admin.ModelAdmin)
admin.site.register(InvasiveSpecies, admin.ModelAdmin)
admin.site.register(HeritageSpecies, admin.ModelAdmin)
admin.site.register(HeritageObservation, admin.ModelAdmin)
admin.site.register(FishSpecies, admin.ModelAdmin)
admin.site.register(NaturePollution, admin.ModelAdmin)
admin.site.register(TypePollution, admin.ModelAdmin)
