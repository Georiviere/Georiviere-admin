from django.contrib import admin

# Register your models here.
from georiviere.portal.models import Portal


class PortalAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'title')
    search_fields = ('name', 'website')


admin.site.register(Portal, PortalAdmin)
