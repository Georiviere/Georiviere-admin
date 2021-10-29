from django.contrib import admin
from .models import EventType
from geotrek.common.mixins import MergeActionMixin


class EventTypeAdmin(MergeActionMixin, admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', )
    merge_field = "name"


admin.site.register(EventType, EventTypeAdmin)
