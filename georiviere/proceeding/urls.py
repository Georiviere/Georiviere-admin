from .models import Proceeding
from mapentity.registry import registry

app_name = 'proceeding'
urlpatterns = registry.register(Proceeding)
