from django.contrib import admin
from .models import ClassificationWaterPolicy

from geotrek.common.mixins import MergeActionMixin


class ClassificationWaterPolicyAdmin(MergeActionMixin, admin.ModelAdmin):
    list_display = ('label',)
    search_fields = ('label', )
    merge_field = "label"


admin.site.register(ClassificationWaterPolicy, ClassificationWaterPolicyAdmin)
