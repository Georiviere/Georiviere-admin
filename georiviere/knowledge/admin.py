from django.contrib import admin

from georiviere.knowledge.models import (
    VegetationState, VegetationStrata, VegetationType,
    VegetationAgeClassDiversity, VegetationThicknessType, VegetationSpecificDiversity,
    WorkBankEffect, WorkFishContinuityEffect, WorkSedimentEffect,
    WorkWaterEffect, WorkBedEffect,
    WorkStreamInfluence, WorkMaterial, WorkState, WorkType, KnowledgeType,
    FollowUpType
)

admin.site.register(KnowledgeType, admin.ModelAdmin)
admin.site.register(VegetationAgeClassDiversity, admin.ModelAdmin)
admin.site.register(VegetationSpecificDiversity, admin.ModelAdmin)
admin.site.register(VegetationState, admin.ModelAdmin)
admin.site.register(VegetationStrata, admin.ModelAdmin)
admin.site.register(VegetationThicknessType, admin.ModelAdmin)
admin.site.register(VegetationType, admin.ModelAdmin)
admin.site.register(WorkBankEffect, admin.ModelAdmin)
admin.site.register(WorkStreamInfluence, admin.ModelAdmin)
admin.site.register(WorkFishContinuityEffect, admin.ModelAdmin)
admin.site.register(WorkMaterial, admin.ModelAdmin)
admin.site.register(WorkSedimentEffect, admin.ModelAdmin)
admin.site.register(WorkWaterEffect, admin.ModelAdmin)
admin.site.register(WorkBedEffect, admin.ModelAdmin)
admin.site.register(WorkState, admin.ModelAdmin)
admin.site.register(WorkType, admin.ModelAdmin)
admin.site.register(FollowUpType, admin.ModelAdmin)
