from django.contrib import admin

from knowledge.models import (
    Vegetation, VegetationState, VegetationStrata, VegetationType,
    VegetationAgeClassDiversity, VegetationThicknessType, VegetationSpecificDiversity,
    Work, WorkBankEffect, WorkFishContinuityEffect, WorkSedimentEffect,
    WorkStreamInfluence, WorkMaterial, WorkState, WorkType, KnowledgeType,
    FollowUpType
)

admin.site.register(KnowledgeType, admin.ModelAdmin)
admin.site.register(Vegetation)
admin.site.register(VegetationAgeClassDiversity, admin.ModelAdmin)
admin.site.register(VegetationSpecificDiversity, admin.ModelAdmin)
admin.site.register(VegetationState, admin.ModelAdmin)
admin.site.register(VegetationStrata, admin.ModelAdmin)
admin.site.register(VegetationThicknessType, admin.ModelAdmin)
admin.site.register(VegetationType, admin.ModelAdmin)
admin.site.register(Work)
admin.site.register(WorkBankEffect, admin.ModelAdmin)
admin.site.register(WorkStreamInfluence, admin.ModelAdmin)
admin.site.register(WorkFishContinuityEffect, admin.ModelAdmin)
admin.site.register(WorkMaterial, admin.ModelAdmin)
admin.site.register(WorkSedimentEffect, admin.ModelAdmin)
admin.site.register(WorkState, admin.ModelAdmin)
admin.site.register(WorkType, admin.ModelAdmin)
admin.site.register(FollowUpType, admin.ModelAdmin)
