from .models import POIAction, POIKnowledge
from mapentity.registry import registry
from .registry import ValorizationOptions


app_name = 'valorization'
urlpatterns = registry.register(POIKnowledge, options=ValorizationOptions)
urlpatterns += registry.register(POIAction, menu=False)
