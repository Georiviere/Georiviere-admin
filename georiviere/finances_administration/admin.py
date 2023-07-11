from django.contrib import admin

from georiviere.finances_administration.models import (
    Organism, AdministrativeFileType, AdministrativeDeferral, AdministrativeFileDomain,
    AdministrativeOperation, JobCategory
)


admin.site.register(Organism)
admin.site.register(JobCategory)
admin.site.register(AdministrativeFileType)
admin.site.register(AdministrativeFileDomain)
admin.site.register(AdministrativeOperation)
admin.site.register(AdministrativeDeferral)
