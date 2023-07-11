from django.conf import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="Georiviere API valorization",
        default_version='v1',
        description=settings.SWAGGER_SETTINGS["API_PORTAL"],
    ),
    urlconf='georiviere.portal.views.urls',
    public=True,
    permission_classes=(permissions.AllowAny,),
)
