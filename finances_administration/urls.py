from django.urls import path
from mapentity.registry import registry

from finances_administration.models import AdministrativeFile
from finances_administration.views import AdministrativeOperationUpdate


app_name = 'finances_administration'
urlpatterns = registry.register(AdministrativeFile)

urlpatterns += [
    path('administrativeoperation/edit/<int:pk>', AdministrativeOperationUpdate.as_view(), name="administrativeoperation-update")
]
