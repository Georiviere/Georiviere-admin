from .models import Usage, Status, Land, Morphology
from mapentity.registry import registry
from .registry import DescriptionOptions


app_name = 'description'
urlpatterns = registry.register(Usage, options=DescriptionOptions)
urlpatterns += registry.register(Morphology, menu=False)
urlpatterns += registry.register(Status, menu=False)
urlpatterns += registry.register(Land, menu=False)
