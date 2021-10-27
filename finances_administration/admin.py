from django.contrib import admin

from finances_administration.models import (
    Organism, AdministrativeFileType, AdministrativeFileDomain,
    AdministrativeOperation, JobCategory
)


admin.site.register(Organism)
admin.site.register(JobCategory)
admin.site.register(AdministrativeFileType)
admin.site.register(AdministrativeFileDomain)
admin.site.register(AdministrativeOperation)
