from django.conf import settings
from django.urls import path, include
from rest_framework import routers

from georiviere.api.valorization.views import GeoriviereVersionAPIView
from georiviere.api.valorization.views.portal import PortalViewSet
from georiviere.api.valorization.views.river import StreamViewSet
from georiviere.api.valorization.views.swagger import schema_view
from georiviere.api.valorization.views.valorization import POIViewSet
from georiviere.api.valorization.views.zoning import CityViewSet, DistrictViewSet, WatershedViewSet


router = routers.DefaultRouter()
router.register('(?P<portal_pk>\d+)/pois', POIViewSet, basename='pois')

router.register('(?P<portal_pk>\d+)/streams', StreamViewSet, basename='streams')

router.register('portal', PortalViewSet, basename='portal')
router.register('cities', CityViewSet, basename='cities')
router.register('districts', DistrictViewSet, basename='districts')
router.register('watersheds', WatershedViewSet, basename='watersheds')

app_name = 'api_valorization'

_urlpatterns = [
    path('version', GeoriviereVersionAPIView.as_view(), name='version'),
    path('', include(router.urls)),
]
if 'drf_yasg' in settings.INSTALLED_APPS:
    _urlpatterns.append(path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'))
urlpatterns = [path('api/valorization/<lang:lang>/', include(_urlpatterns))]
