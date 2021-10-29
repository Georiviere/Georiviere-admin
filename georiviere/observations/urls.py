from .models import Station
from mapentity.registry import registry

app_name = 'observations'
urlpatterns = registry.register(Station)
