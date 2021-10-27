from .models import Knowledge, FollowUp
from mapentity.registry import registry

app_name = 'knowledge'
urlpatterns = registry.register(Knowledge)
urlpatterns += registry.register(FollowUp)
