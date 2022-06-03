from django.contrib import admin

from .models import FileType, DataSource

admin.site.register(FileType)
admin.site.register(DataSource)
