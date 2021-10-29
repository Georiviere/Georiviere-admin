from georiviere.maintenance.models import Intervention
from mapentity.registry import registry

app_name = 'maintenance'
urlpatterns = registry.register(Intervention)
