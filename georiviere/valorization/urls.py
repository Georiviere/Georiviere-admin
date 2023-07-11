from .models import POI
from mapentity.registry import registry
from .registry import ValorizationOptions


app_name = 'valorization'
urlpatterns = registry.register(POI, options=ValorizationOptions)
