from studies.models import Study
from mapentity.registry import registry

app_name = 'studies'
urlpatterns = registry.register(Study)
