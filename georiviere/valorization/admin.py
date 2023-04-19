from django.contrib import admin

from georiviere.valorization.models import POIActionType, POIKnowledgeType


class POIKnowledgeTypeAdmin(admin.ModelAdmin):
    list_display = ('label',)
    search_fields = ('label',)


class POIActionTypeAdmin(admin.ModelAdmin):
    list_display = ('label',)
    search_fields = ('label',)


admin.site.register(POIKnowledgeType, POIKnowledgeTypeAdmin)
admin.site.register(POIActionType, POIActionTypeAdmin)
